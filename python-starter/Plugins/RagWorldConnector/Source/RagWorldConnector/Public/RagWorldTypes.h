#pragma once

#include "CoreMinimal.h"
#include "RagWorldTypes.generated.h"

USTRUCT(BlueprintType)
struct RAGWORLDCONNECTOR_API FRagWorldAsset
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Kind;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Url;
};

USTRUCT(BlueprintType)
struct RAGWORLDCONNECTOR_API FRagWorldJob
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Id;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Status;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Provider;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Error;
};

USTRUCT(BlueprintType)
struct RAGWORLDCONNECTOR_API FRagGeneratedWorld
{
    GENERATED_BODY()

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Id;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Status;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Provider;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Caption;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    FString Error;

    UPROPERTY(BlueprintReadOnly, Category = "RAG World")
    TArray<FRagWorldAsset> Assets;
};
