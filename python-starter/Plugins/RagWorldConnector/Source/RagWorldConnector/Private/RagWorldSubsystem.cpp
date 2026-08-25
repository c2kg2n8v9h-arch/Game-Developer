#include "RagWorldSubsystem.h"

#include "Dom/JsonObject.h"
#include "GenericPlatform/GenericPlatformHttp.h"
#include "HttpModule.h"
#include "Interfaces/IHttpRequest.h"
#include "Interfaces/IHttpResponse.h"
#include "Serialization/JsonReader.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"

URagWorldSubsystem::URagWorldSubsystem()
    : ServiceBaseUrl(TEXT("http://127.0.0.1:8000"))
{
}

void URagWorldSubsystem::GenerateWorld(
    const FString& Description,
    const FString& DisplayName,
    const FString& SourceImageUrl
)
{
    if (Description.TrimStartAndEnd().IsEmpty())
    {
        OnRequestFailed.Broadcast(0, TEXT("World description cannot be empty."));
        return;
    }

    const TSharedRef<FJsonObject> Body = MakeShared<FJsonObject>();
    Body->SetStringField(TEXT("description"), Description);
    if (!DisplayName.IsEmpty())
    {
        Body->SetStringField(TEXT("display_name"), DisplayName);
    }
    if (!SourceImageUrl.IsEmpty())
    {
        Body->SetStringField(TEXT("source_image_url"), SourceImageUrl);
    }
    Body->SetObjectField(TEXT("metadata"), MakeShared<FJsonObject>());

    FString JsonBody;
    const TSharedRef<TJsonWriter<>> Writer = TJsonWriterFactory<>::Create(&JsonBody);
    FJsonSerializer::Serialize(Body, Writer);

    const TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(BuildUrl(TEXT("/v1/worlds")));
    Request->SetVerb(TEXT("POST"));
    Request->SetHeader(TEXT("Content-Type"), TEXT("application/json"));
    Request->SetContentAsString(JsonBody);
    Request->SetTimeout(30.0f);
    Request->OnProcessRequestComplete().BindUObject(this, &URagWorldSubsystem::HandleCreateResponse);
    Request->ProcessRequest();
}

void URagWorldSubsystem::GetWorld(const FString& WorldId, const bool bPersistManifest)
{
    if (WorldId.IsEmpty())
    {
        OnRequestFailed.Broadcast(0, TEXT("World ID cannot be empty."));
        return;
    }

    const FString Path = FString::Printf(
        TEXT("/v1/worlds/%s?persist_manifest=%s"),
        *FGenericPlatformHttp::UrlEncode(WorldId),
        bPersistManifest ? TEXT("true") : TEXT("false")
    );
    const TSharedRef<IHttpRequest, ESPMode::ThreadSafe> Request = FHttpModule::Get().CreateRequest();
    Request->SetURL(BuildUrl(Path));
    Request->SetVerb(TEXT("GET"));
    Request->SetTimeout(30.0f);
    Request->OnProcessRequestComplete().BindUObject(this, &URagWorldSubsystem::HandleGetResponse);
    Request->ProcessRequest();
}

void URagWorldSubsystem::HandleCreateResponse(
    FHttpRequestPtr Request,
    FHttpResponsePtr Response,
    const bool bSucceeded
)
{
    if (!bSucceeded || !Response.IsValid() || !EHttpResponseCodes::IsOk(Response->GetResponseCode()))
    {
        BroadcastHttpError(Response, bSucceeded);
        return;
    }

    TSharedPtr<FJsonObject> Json;
    const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());
    if (!FJsonSerializer::Deserialize(Reader, Json) || !Json.IsValid())
    {
        OnRequestFailed.Broadcast(Response->GetResponseCode(), TEXT("Invalid create-world response."));
        return;
    }

    FRagWorldJob Job;
    Json->TryGetStringField(TEXT("id"), Job.Id);
    Json->TryGetStringField(TEXT("status"), Job.Status);
    Json->TryGetStringField(TEXT("provider"), Job.Provider);
    Json->TryGetStringField(TEXT("error"), Job.Error);
    OnWorldJobCreated.Broadcast(Job);
}

void URagWorldSubsystem::HandleGetResponse(
    FHttpRequestPtr Request,
    FHttpResponsePtr Response,
    const bool bSucceeded
)
{
    if (!bSucceeded || !Response.IsValid() || !EHttpResponseCodes::IsOk(Response->GetResponseCode()))
    {
        BroadcastHttpError(Response, bSucceeded);
        return;
    }

    TSharedPtr<FJsonObject> Json;
    const TSharedRef<TJsonReader<>> Reader = TJsonReaderFactory<>::Create(Response->GetContentAsString());
    if (!FJsonSerializer::Deserialize(Reader, Json) || !Json.IsValid())
    {
        OnRequestFailed.Broadcast(Response->GetResponseCode(), TEXT("Invalid world response."));
        return;
    }

    FRagGeneratedWorld World;
    Json->TryGetStringField(TEXT("id"), World.Id);
    Json->TryGetStringField(TEXT("status"), World.Status);
    Json->TryGetStringField(TEXT("provider"), World.Provider);
    Json->TryGetStringField(TEXT("caption"), World.Caption);
    Json->TryGetStringField(TEXT("error"), World.Error);

    const TArray<TSharedPtr<FJsonValue>>* Assets;
    if (Json->TryGetArrayField(TEXT("assets"), Assets))
    {
        for (const TSharedPtr<FJsonValue>& Value : *Assets)
        {
            const TSharedPtr<FJsonObject> AssetJson = Value->AsObject();
            if (!AssetJson.IsValid())
            {
                continue;
            }
            FRagWorldAsset Asset;
            AssetJson->TryGetStringField(TEXT("kind"), Asset.Kind);
            AssetJson->TryGetStringField(TEXT("url"), Asset.Url);
            World.Assets.Add(MoveTemp(Asset));
        }
    }
    OnWorldReceived.Broadcast(World);
}

FString URagWorldSubsystem::BuildUrl(const FString& Path) const
{
    FString Base = ServiceBaseUrl;
    Base.RemoveFromEnd(TEXT("/"));
    return Base + Path;
}

void URagWorldSubsystem::BroadcastHttpError(
    const FHttpResponsePtr& Response,
    const bool bSucceeded
)
{
    const int32 StatusCode = Response.IsValid() ? Response->GetResponseCode() : 0;
    const FString Message = Response.IsValid()
        ? Response->GetContentAsString()
        : (bSucceeded ? TEXT("Empty HTTP response.") : TEXT("Could not reach the RAG service."));
    OnRequestFailed.Broadcast(StatusCode, Message);
}
