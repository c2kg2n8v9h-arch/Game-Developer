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

## Minimal runnable demo

1. Start the local service from the repository's `python-starter` directory:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -e ".[dev]"
   python -m rag_service
   ```

   On macOS/Linux, activate with `source .venv/bin/activate` instead.

2. Open `GameDeveloper.uproject` in Unreal Engine, compile when prompted, and create or open any level.
3. Drag **Rag World Demo Actor** from the Place Actors panel into the level. Rotate/position it so its Text Render components face the player camera.
4. Press Play. The actor submits its editable **World Description**, polls the job, and displays **Status**, **Caption**, and **Manifest** in the world.

`Submit World` is also Blueprint-callable, so a Level Blueprint or UI button can rerun the demo. The local provider is deterministic and requires no credentials. For remote providers, configure keys only in the Python service environment; the Unreal plugin sends no provider credentials.
