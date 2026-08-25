using UnrealBuildTool;
using System.Collections.Generic;

public class GameDeveloperTarget : TargetRules
{
    public GameDeveloperTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        ExtraModuleNames.Add("GameDeveloper");
    }
}
