# precorder

A recorder that keeps recording into an in-memory buffer, so when you hear something burst out you can write the buffer into a file and not lose any highlights.


## Setup

```powershell
PS > poetry install
PS > poetry env activate | iwr      # I'm using pwsh so change this if this does not match with your shell
```

## Run

```
(precorder-py3.13) PS > py main.py
```

This will start a recorder process which immediates starts recording. Enter some command to interact with the recorder proces:  

- `s`: Start a new record and write all the frames in buffer to this record
- `t`: Stop current record
- `i`: Show current buffer size and some other information
- `q`: Quit (Does not save current buffer)

## Trivia

### Why?

The idea originally comes to me when trying to record my roommates' noises when they were playing Valorant.  
