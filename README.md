# DO_ALL_THE_THINGS

initialization script for AD CTF (init repos, SAST, and more)

## Structure

- main.py - router
- utils.py - utility layer
- scenarious - directory to store different scenarious (init, sast etc.)
- scenarios/*_funcs.py - func files for scenarios

## Usage

```bash
git clone https://github.com/SgffCTF/DO_ALL_THE_THINGS
python3 -m venv venv
source venv/bin/activate
python3 main.py <scenario> <options>
```