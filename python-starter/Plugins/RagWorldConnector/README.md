# RAG World Connector

Runtime Unreal Engine plugin for the Python RAG/world-generation API.

## Install

1. Copy `RagWorldConnector` into your Unreal project's `Plugins` directory.
2. Regenerate project files and compile the project.
3. Enable **RAG World Connector** under **Edit > Plugins > AI**.
4. Restart Unreal Editor.

The subsystem is available from Blueprint through **Get Game Instance Subsystem** using `RagWorldSubsystem`.

Call `Generate World`, handle `On World Job Created`, and poll `Get World` with a timer until the status is `succeeded` or `failed`. The backend URL defaults to `http://127.0.0.1:8000` and can be changed on the subsystem or through project configuration.

Do not place provider API keys in Unreal. Keep them in the Python service environment.
