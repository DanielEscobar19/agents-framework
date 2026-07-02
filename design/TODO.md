- check if this architecture is reusabel with cluad code or otehr ones (it is beacuse we are creating a mcp server)

- No chunk-level diffing (full file re-embedding on change)
  - check teh chunking policy to know which to use (now ses every 40 lines not ideal) in progress
  - update only chunks isntead of the whole file next stpe

- add full rebuidl index option

- add control loggin level with config object form teh appsettings

- No async indexing pipeline
- No embedding cache layer
- No retrieval API yet
