# DO_ALL_THE_THINGS

initialization script for AD CTF (init repos, SAST, and more)

## Structure

- main_script.py - router
- utils.py - utility layer
- scenarious - directory to store different scenarious (init, sast etc.)
- scenarios/*_funcs.py - func files for scenarios

## Usage

```bash
curl -L $(curl -s https://api.github.com/repos/SgffCTF/DO_ALL_THE_THINGS/releases/latest | grep browser_download_url | cut -d '"' -f 4) -o datt.zip
python3 -m venv venv
source venv/bin/activate
python3 datt.zip \<scenario> \<options>
```