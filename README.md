<a name="readme-top"></a>

<br />
<div align="center">
  <a href="https://github.com/thomasmichaelkane/ao_cropper">
    <img src="docs/images/ao_cropper.gif" alt="Logo" width="200">
  </a>

  <h3 align="center">ao_cropper</h3>

  <p align="center">
    Easily crop subsections from AOSLO images with auto-scaling
    <br />
    <a href="https://github.com/thomasmichaelkane/ao_cropper/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/thomasmichaelkane/ao_cropper/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

---

## About

ao_cropper is a desktop tool for efficiently cropping and scaling sections of large AOSLO retinal images. It provides a maps-style zoomable canvas where you place a foveal centre point and an unlimited number of crop boxes with a double-click. All crop coordinates are automatically calculated in degrees and microns relative to the foveal centre. On save, labelled crop TIFFs, annotated overview maps, and a CSV of crop metadata are written for every imaging modality found in the folder.

---

## Installation

This project uses [uv](https://docs.astral.sh/uv/) for package and environment management.

1. Clone the repository
   ```sh
   git clone https://github.com/thomasmichaelkane/ao_cropper.git
   cd ao_cropper
   ```

2. Install dependencies
   ```sh
   uv sync
   ```

---

## Running

```sh
uv run ao-cropper <image_path> <OD|OS>
```

`image_path` should point to a single-layer TIFF file. `eye` is the side being imaged — `OD` (right) or `OS` (left).

Optional flags let you override per-patient acquisition parameters without editing the config file:

| Flag | Short | Description |
|---|---|---|
| `--axial-length MM` | `-a` | Patient axial length in mm |
| `--mpp UM/PX` | `-m` | Microns per pixel from image metadata |
| `--locate` | `-l` | Save maps only — skips extracting individual crops, useful for reviewing placement before a final run |

Run `uv run ao-cropper --help` for full usage.

**Image file naming convention:** files should follow the pattern `<ID>_<other_info>_<MODALITY>.tif` (e.g. `MM_0364_OS_0p38umpx_split.tif`). All TIFFs in the same folder sharing the same base name are treated as additional modalities and cropped simultaneously on save.

**Defaults and settings** (crop size, colours, font sizes, etc.) are configured in `config.yaml` at the project root. The tool must be run from the project root directory so that `config.yaml` can be found — running it from another directory will cause an error on startup.

---

## Usage

ao_cropper provides a two-window interface: a zoomable canvas for placing crops, and a control panel showing crop coordinates and save controls. Full usage instructions are available in the [documentation](#).

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

## Contact

Thomas Kane — thomas.kane.ucl@gmail.com — [thomasmichaelkane.github.io/me](https://thomasmichaelkane.github.io/me/)

Project link: [github.com/thomasmichaelkane/ao_cropper](https://github.com/thomasmichaelkane/ao_cropper)

<p align="right">(<a href="#readme-top">back to top</a>)</p>
