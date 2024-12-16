## Overall Concept

A CLI tool (frontend) that interacts with a backend to manage data processing pipelines. Pipelines are defined by a JSON configuration file that specifies nodes (scripts and datasets) and edges (connections with arguments). The system supports local versions, sharing to a catalog, synchronization with the catalog, and generation of runnable scripts.

## Storage and Home Folder

- **DATA_FACTORY_HOME**:  
  - If `DATA_FACTORY_HOME` is not set, default to `~/data-factory-home`.
  - Inside `DATA_FACTORY_HOME`, the CLI stores internal state and versions of pipelines.
  - The directory structure:
    ```
    ~/data-factory-home/
    ├─ pipelines/
    │  ├─ abc123_1.json
    │  ├─ abc123_2.json
    │  ├─ abc123_state.json
    │  ...
    ```
  - `abc123` is an example pipeline `id` (UUID-based).
  - `abc123_state.json` tracks `latest_version` and `versions` as a key-value map:
    ```json
    {
      "latest_version": 2,
      "versions": {
        "1": "abc123_1.json",
        "2": "abc123_2.json"
      }
    }
    ```

- **Token/Config File for Authentication (If Needed)**:  
  - The CLI may read a config file from `DATA_FACTORY_HOME/config.ini` or `DATA_FACTORY_HOME/config.json` to retrieve a JWT token or other credentials if required.
  - This is optional

## Pipeline Configuration File Format

- **Pipeline Top-Level Fields**:
  - `id`: Unique pipeline ID assigned at creation (e.g., `"abc123"`).
  - `nodes`: Array of nodes, each with:
    - `id`: User-assigned node identifier, used for internal graph references.
    - `type`: `"script"` or `"dataset"`.
    - For scripts:
      - `script_id` (if catalog-based) or `path` (if local).
    - For datasets:
      - `dataset_id` (if catalog-based) or `path` (if local).
  - `edges`: Array of edges, each with:
    - `from`: Node `id` of the source.
    - `to`: Node `id` of the target.
    - `arguments`: Array of arguments to pass. Arguments can be strings or objects like `{ "ref": "node_id" }` to reference nodes by `id`.

- **Catalogue Version**:  
    - After sharing and syncing, scripts and datasets have `script_id`/`dataset_id`.
    - Edges may still reference `{ "ref": "node_id" }`, but the backend resolves these `id` references.
    - Or after a `sync`, the CLI could rewrite arguments to use `dataset_id` directly if desired.

- **ID for Graph Management**:
  - Each node has a user-assigned `id` used in `from`/`to` fields in edges.
  - The pipeline `id` is assigned by CLI and identifies the pipeline globally in local and catalog storage.

## Commands

1. **Create**:  
   ```bash
   data-factory-cli create user_pipeline.json
   ```
   - Reads `user_pipeline.json`.
   - If no pipeline `id`, assign `id = abc123`.
   - Saves `abc123_1.json` and `abc123_state.json` in `DATA_FACTORY_HOME/pipelines/`.
   - Updates `user_pipeline.json` to include the pipeline `id`.
   - Prints the pipeline `id`.

2. **Update**:  
   ```bash
   data-factory-cli update user_pipeline.json
   ```
   - Reads the `id` from `user_pipeline.json`.
   - Increments local version, e.g., `abc123_2.json`.
   - Updates state file with new version.
   - `user_pipeline.json` remains the user's working file.

3. **Share**:
   Two modes:
   - By file:
     ```bash
     data-factory-cli share -f user_pipeline.json [--token <JWT>]
     ```
     Shares the pipeline defined in `user_pipeline.json` as-is, creating a new remote version.
   
   - By id/version:
     ```bash
     data-factory-cli pipeline share -i abc123 [-v VERSION] [--token <JWT>]
     ```
     Shares a previously stored local version from `DATA_FACTORY_HOME/pipelines/`.
     If no `-v` given, share the latest version.
     
   Each share appends a new remote version in the catalog.

4. **List**:
   ```bash
   data-factory-cli list pipelines
   data-factory-cli list scripts
   data-factory-cli list datasets
   ```
   Lists available pipelines, scripts, and datasets.
   - Pipelines: Lists IDs from local store and/or remote catalog.
   - Scripts/Datasets: Placeholder or fetch from backend.
   - Filter and search options can be added.

5. **Sync**:  
   ```bash
   data-factory-cli sync user_pipeline.json [--version N]
   ```
   - Reads `id` from `user_pipeline.json`.
   - Fetches the pipeline from the catalog (the specified version or latest).
   - Overwrites `user_pipeline.json` with the catalog’s version, ensuring scripts and datasets have `script_id`/`dataset_id`.
   - This converts local references (`path`) into catalog references if the backend provides them.

6. **Generate**:  
   ```bash
   data-factory-cli generate -f user_pipeline.json
   ```
   or
   ```bash
   data-factory-cli generate -i abc123 [-v VERSION]
   ```
   - `generate` produces a runnable script that encapsulates the entire launch workflow:
     - Fetching or preparing datasets.
     - Running scripts with given arguments from edges.
   - If `-f` is used, it uses the pipeline defined in that file.
   - If `-i` is used with `-v`, it uses a specific local version from `DATA_FACTORY_HOME`.
   - If the pipeline or script is in the catalog, `generate` might also handle pulling necessary files or setting up the environment as described by the pipeline.
   
   The generated script should allow the user to run the pipeline anywhere by executing this one generated shell script.

## Workflow

- **Initialization**:
  - User starts with a local `user_pipeline.json` without `id`.
  - `create` assigns `id`, sets up first version, updates `user_pipeline.json`.

- **Iteration**:
  - User edits `user_pipeline.json`, runs `update` to record changes locally.
  - User can `share` to publish versions to the catalog.
  - After sharing, `sync` can be used to align local file with catalog references.
  - The user can `generate` a runnable script from any state (file or id/version).

- **Arguments and References**:
  - `arguments` on edges can contain `{ "ref": "node_id" }` to reference nodes. The backend or the CLI (on sync) may eventually resolve these.
  - Initially, nodes may have `path`. After sharing/syncing, they may gain `script_id` or `dataset_id`.
  
- **No Overwrites in Catalog**:
  - Every `share` command creates a new remote version. The pipeline version history grows append-only.