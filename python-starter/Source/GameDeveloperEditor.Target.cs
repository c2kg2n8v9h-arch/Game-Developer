using UnrealBuildTool;
using System.Collections.Generic;

public class GameDeveloperEditorTarget : TargetRules
{
    public GameDeveloperEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        ExtraModuleNames.Add("GameDeveloper");
    }
}
