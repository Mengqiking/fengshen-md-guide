"""Launch the verified Chinese Mega Drive release using an isolated RetroArch config."""
import argparse
import hashlib
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIZE = 2097152
SHA256 = "870e1e55b356d76adf95c50dcafc52021572293224ab537217f9842ccba2fc85"


def matches(path):
    return (path.is_file() and path.stat().st_size == SIZE
            and hashlib.sha256(path.read_bytes()).hexdigest() == SHA256)


def find_rom(explicit):
    if explicit:
        if matches(explicit):
            return explicit.resolve()
        raise ValueError("指定文件与已验证的台湾中文 MD 镜像不匹配。请先解压，再核对版本。")
    folder = ROOT / "roms"
    if folder.is_dir():
        for path in sorted(folder.iterdir()):
            if path.suffix.lower() in {".md", ".bin", ".gen"} and matches(path):
                return path.resolve()
    raise ValueError(f"请把自己合法取得的原版裸 ROM 放入 {folder}，再运行一次。")


def require_file(path, label):
    if path is None or not Path(path).is_file():
        raise ValueError(f"找不到{label}。请参照 README 安装，或通过命令行指定路径。")
    return Path(path).resolve()


def write_config(data, emulator, core, rom):
    dirs = {"savefile_directory": "saves", "savestate_directory": "states",
            "screenshot_directory": "screenshots", "log_dir": "logs",
            "system_directory": "system", "core_options_path": "config/core-options.cfg",
            "menu_config_directory": "config", "input_remapping_directory": "remaps",
            "playlist_directory": "playlists", "content_history_directory": "playlists"}
    config = (ROOT / "fengshen.cfg").read_text(encoding="utf-8")
    paths = {}
    for setting, name in dirs.items():
        path = data / name
        folder = path.parent if setting == "core_options_path" else path
        folder.mkdir(parents=True, exist_ok=True)
        paths[setting] = path
    paths["libretro_directory"] = core.parent
    paths["rgui_browser_directory"] = rom.parent
    for name, setting in [("assets", "assets_directory"), ("info", "libretro_info_path")]:
        if (emulator.parent / name).is_dir():
            paths[setting] = emulator.parent / name
    if sys.platform == "win32":
        config += '\nvideo_driver = "d3d11"\n'
    for setting, path in paths.items():
        value = path.as_posix()
        if any(ch in value for ch in '"\r\n'):
            raise ValueError("路径含有配置文件无法表示的字符。")
        config += f'{setting} = "{value}"\n'
    target = data / "retroarch.cfg"
    target.write_text(config, encoding="utf-8")
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rom", type=Path)
    parser.add_argument("--retroarch", type=Path)
    parser.add_argument("--core", type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="只核对文件与游戏版本")
    mode.add_argument("--verify", action="store_true", help="隔离运行 900 帧并保存截图")
    args = parser.parse_args()
    rom = find_rom(args.rom)
    windows = sys.platform == "win32"
    default_exe = ROOT / "RetroArch-Win64" / "retroarch.exe" if windows else shutil.which("retroarch")
    emulator = require_file(args.retroarch or default_exe, " RetroArch")
    ext = "dll" if windows else "dylib" if sys.platform == "darwin" else "so"
    core = require_file(args.core or emulator.parent / "cores" / f"genesis_plus_gx_libretro.{ext}", " Genesis Plus GX 核心")
    print(f"ROM 校验通过：{rom.name}\nSHA-256 {SHA256}", flush=True)
    if args.check:
        print(f"模拟器：{emulator}\n核心：{core}")
        return 0
    data = ROOT / "runtime"
    if args.verify:
        checks = data / "checks"
        checks.mkdir(parents=True, exist_ok=True)
        data = Path(tempfile.mkdtemp(prefix="run-", dir=checks))
    cfg = write_config(data, emulator, core, rom)
    log = data / "logs" / "retroarch.log"
    cmd = [str(emulator), "--config", str(cfg), "--verbose", "--log-file", str(log), "-L", str(core)]
    shot = data / "screenshots" / "opening.png"
    if args.verify:
        cmd.extend(["--max-frames", "900", "--max-frames-ss", "--max-frames-ss-path", str(shot)])
    print(f"日志：{log}", flush=True)
    result = subprocess.run([*cmd, str(rom)], cwd=emulator.parent, timeout=120 if args.verify else None)
    if result.returncode:
        if log.is_file() and "An Application Control policy has blocked this file" in log.read_text(
                encoding="utf-8", errors="replace"):
            raise ValueError("Windows 应用控制拦截了核心 DLL。请使用设备策略允许的核心版本；详情见日志。")
        raise ValueError(f"RetroArch 退出码 {result.returncode}。请查看日志。")
    if args.verify:
        if not shot.is_file() or not shot.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("未取得游戏截图，请查看本次日志。")
        print(f"已生成截图，请打开核对繁体剧情：{shot}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        sys.exit(str(error))
