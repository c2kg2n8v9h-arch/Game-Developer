#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "RagWorldTypes.h"
#include "TimerManager.h"
#include "RagWorldDemoActor.generated.h"

class UTextRenderComponent;
class URagWorldSubsystem;

/**
 * Drop-in, Blueprint-friendly demo for the local RAG world service.
 * Place the actor in a level and press Play to submit, poll, and display a result.
 */
UCLASS(Blueprintable)
class RAGWORLDCONNECTOR_API ARagWorldDemoActor : public AActor
{
    GENERATED_BODY()

public:
    ARagWorldDemoActor();

    virtual void BeginPlay() override;
    virtual void EndPlay(const EEndPlayReason::Type EndPlayReason) override;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RAG World|Demo", meta = (MultiLine = true))
    FString WorldDescription = TEXT("A small moonlit island with ancient ruins and glowing trees");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RAG World|Demo")
    FString DisplayName = TEXT("RAG Demo World");

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RAG World|Demo")
    FString SourceImageUrl;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RAG World|Demo")
    bool bSubmitOnBeginPlay = true;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RAG World|Demo", meta = (ClampMin = "0.1"))
    float PollIntervalSeconds = 1.0f;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "RAG World|Demo", meta = (ClampMin = "32"))
    int32 MaxCaptionCharacters = 500;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RAG World|Demo")
    FString JobStatus;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RAG World|Demo")
    FString Caption;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RAG World|Demo")
    FString ManifestUrl;

    UFUNCTION(BlueprintCallable, Category = "RAG World|Demo")
    void SubmitWorld();

protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RAG World|Demo")
    TObjectPtr<UTextRenderComponent> StatusText;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RAG World|Demo")
    TObjectPtr<UTextRenderComponent> CaptionText;

    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "RAG World|Demo")
    TObjectPtr<UTextRenderComponent> ManifestText;

private:
    UFUNCTION()
    void HandleJobCreated(const FRagWorldJob& Job);

    UFUNCTION()
    void HandleWorldReceived(const FRagGeneratedWorld& World);

    UFUNCTION()
    void HandleRequestFailed(int32 StatusCode, const FString& Message);

    void PollWorld();
    void RefreshText();
    URagWorldSubsystem* GetRagSubsystem() const;

    FString ActiveWorldId;
    FTimerHandle PollTimerHandle;
};
