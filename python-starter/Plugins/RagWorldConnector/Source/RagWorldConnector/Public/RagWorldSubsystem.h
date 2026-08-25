#pragma once

#include "CoreMinimal.h"
#include "HttpFwd.h"
#include "Subsystems/GameInstanceSubsystem.h"
#include "RagWorldTypes.h"
#include "RagWorldSubsystem.generated.h"

DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FRagWorldJobCreated, const FRagWorldJob&, Job);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_OneParam(FRagWorldReceived, const FRagGeneratedWorld&, World);
DECLARE_DYNAMIC_MULTICAST_DELEGATE_TwoParams(FRagWorldRequestFailed, int32, StatusCode, const FString&, Message);

UCLASS(Config = Game)
class RAGWORLDCONNECTOR_API URagWorldSubsystem : public UGameInstanceSubsystem
{
    GENERATED_BODY()

public:
    URagWorldSubsystem();

    UPROPERTY(Config, EditAnywhere, BlueprintReadWrite, Category = "RAG World|Connection")
    FString ServiceBaseUrl;

    UPROPERTY(BlueprintAssignable, Category = "RAG World|Events")
    FRagWorldJobCreated OnWorldJobCreated;

    UPROPERTY(BlueprintAssignable, Category = "RAG World|Events")
    FRagWorldReceived OnWorldReceived;

    UPROPERTY(BlueprintAssignable, Category = "RAG World|Events")
    FRagWorldRequestFailed OnRequestFailed;

    UFUNCTION(BlueprintCallable, Category = "RAG World")
    void GenerateWorld(
        const FString& Description,
        const FString& DisplayName,
        const FString& SourceImageUrl
    );

    UFUNCTION(BlueprintCallable, Category = "RAG World")
    void GetWorld(const FString& WorldId, bool bPersistManifest = false);

private:
    void HandleCreateResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSucceeded);
    void HandleGetResponse(FHttpRequestPtr Request, FHttpResponsePtr Response, bool bSucceeded);
    FString BuildUrl(const FString& Path) const;
    void BroadcastHttpError(const FHttpResponsePtr& Response, bool bSucceeded);
};
