#include "RagWorldDemoActor.h"

#include "Components/SceneComponent.h"
#include "Components/TextRenderComponent.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "RagWorldSubsystem.h"
#include "TimerManager.h"

ARagWorldDemoActor::ARagWorldDemoActor()
{
    PrimaryActorTick.bCanEverTick = false;

    USceneComponent* SceneRoot = CreateDefaultSubobject<USceneComponent>(TEXT("Root"));
    SetRootComponent(SceneRoot);

    StatusText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("StatusText"));
    StatusText->SetupAttachment(SceneRoot);
    StatusText->SetWorldSize(32.0f);
    StatusText->SetTextRenderColor(FColor(255, 210, 64));

    CaptionText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("CaptionText"));
    CaptionText->SetupAttachment(SceneRoot);
    CaptionText->SetRelativeLocation(FVector(0.0, 0.0, -50.0));
    CaptionText->SetWorldSize(22.0f);
    CaptionText->SetTextRenderColor(FColor::White);

    ManifestText = CreateDefaultSubobject<UTextRenderComponent>(TEXT("ManifestText"));
    ManifestText->SetupAttachment(SceneRoot);
    ManifestText->SetRelativeLocation(FVector(0.0, 0.0, -100.0));
    ManifestText->SetWorldSize(18.0f);
    ManifestText->SetTextRenderColor(FColor(100, 200, 255));

    JobStatus = TEXT("Idle");
}

void ARagWorldDemoActor::BeginPlay()
{
    Super::BeginPlay();

    if (URagWorldSubsystem* Subsystem = GetRagSubsystem())
    {
        Subsystem->OnWorldJobCreated.AddDynamic(this, &ARagWorldDemoActor::HandleJobCreated);
        Subsystem->OnWorldReceived.AddDynamic(this, &ARagWorldDemoActor::HandleWorldReceived);
        Subsystem->OnRequestFailed.AddDynamic(this, &ARagWorldDemoActor::HandleRequestFailed);
    }

    RefreshText();
    if (bSubmitOnBeginPlay)
    {
        SubmitWorld();
    }
}

void ARagWorldDemoActor::EndPlay(const EEndPlayReason::Type EndPlayReason)
{
    GetWorldTimerManager().ClearTimer(PollTimerHandle);
    if (URagWorldSubsystem* Subsystem = GetRagSubsystem())
    {
        Subsystem->OnWorldJobCreated.RemoveDynamic(this, &ARagWorldDemoActor::HandleJobCreated);
        Subsystem->OnWorldReceived.RemoveDynamic(this, &ARagWorldDemoActor::HandleWorldReceived);
        Subsystem->OnRequestFailed.RemoveDynamic(this, &ARagWorldDemoActor::HandleRequestFailed);
    }
    Super::EndPlay(EndPlayReason);
}

void ARagWorldDemoActor::SubmitWorld()
{
    URagWorldSubsystem* Subsystem = GetRagSubsystem();
    if (!Subsystem)
    {
        HandleRequestFailed(0, TEXT("RagWorldSubsystem is unavailable."));
        return;
    }

    GetWorldTimerManager().ClearTimer(PollTimerHandle);
    ActiveWorldId.Reset();
    Caption.Reset();
    ManifestUrl.Reset();
    JobStatus = TEXT("Submitting");
    RefreshText();
    Subsystem->GenerateWorld(WorldDescription, DisplayName, SourceImageUrl);
}

void ARagWorldDemoActor::HandleJobCreated(const FRagWorldJob& Job)
{
    ActiveWorldId = Job.Id;
    JobStatus = Job.Status.IsEmpty() ? TEXT("Queued") : Job.Status;
    RefreshText();

    // Always fetch once: even the local provider returns "succeeded" at creation,
    // while caption and manifest are supplied by the detail endpoint.
    PollWorld();
}

void ARagWorldDemoActor::PollWorld()
{
    if (URagWorldSubsystem* Subsystem = GetRagSubsystem())
    {
        Subsystem->GetWorld(ActiveWorldId, false);
    }
}

void ARagWorldDemoActor::HandleWorldReceived(const FRagGeneratedWorld& World)
{
    if (World.Id != ActiveWorldId)
    {
        return;
    }

    JobStatus = World.Status;
    Caption = World.Caption;
    ManifestUrl.Reset();
    for (const FRagWorldAsset& Asset : World.Assets)
    {
        if (Asset.Kind.Equals(TEXT("manifest"), ESearchCase::IgnoreCase))
        {
            ManifestUrl = Asset.Url;
            break;
        }
    }
    RefreshText();

    if (JobStatus.Equals(TEXT("succeeded"), ESearchCase::IgnoreCase)
        || JobStatus.Equals(TEXT("failed"), ESearchCase::IgnoreCase))
    {
        GetWorldTimerManager().ClearTimer(PollTimerHandle);
        return;
    }

    GetWorldTimerManager().SetTimer(
        PollTimerHandle,
        this,
        &ARagWorldDemoActor::PollWorld,
        FMath::Max(0.1f, PollIntervalSeconds),
        false
    );
}

void ARagWorldDemoActor::HandleRequestFailed(const int32 StatusCode, const FString& Message)
{
    GetWorldTimerManager().ClearTimer(PollTimerHandle);
    JobStatus = StatusCode > 0
        ? FString::Printf(TEXT("Request failed (HTTP %d)"), StatusCode)
        : TEXT("Request failed");
    Caption = Message;
    RefreshText();
}

void ARagWorldDemoActor::RefreshText()
{
    StatusText->SetText(FText::FromString(FString::Printf(TEXT("Status: %s"), *JobStatus)));

    FString DisplayCaption = Caption.IsEmpty() ? TEXT("Waiting for caption...") : Caption;
    const int32 CaptionLimit = FMath::Max(32, MaxCaptionCharacters);
    if (DisplayCaption.Len() > CaptionLimit)
    {
        DisplayCaption = DisplayCaption.Left(CaptionLimit) + TEXT("...");
    }
    CaptionText->SetText(FText::FromString(FString::Printf(TEXT("Caption: %s"), *DisplayCaption)));
    ManifestText->SetText(FText::FromString(FString::Printf(
        TEXT("Manifest: %s"),
        ManifestUrl.IsEmpty() ? TEXT("Waiting for manifest...") : *ManifestUrl
    )));
}

URagWorldSubsystem* ARagWorldDemoActor::GetRagSubsystem() const
{
    const UWorld* World = GetWorld();
    UGameInstance* GameInstance = World ? World->GetGameInstance() : nullptr;
    return GameInstance ? GameInstance->GetSubsystem<URagWorldSubsystem>() : nullptr;
}
