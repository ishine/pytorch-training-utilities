import matplotlib.pyplot as plt
from collections import defaultdict

from .trainer import get_cfg, get_iteration


def is_saving():
    cfg = get_cfg()
    itr = get_iteration()
    return (
        cfg is not None
        and cfg.save_artifact_every is not None
        and itr is not None
        and itr % cfg.save_artifact_every == 0
    )


def get_cfg_itr_strict():
    assert is_saving()
    cfg = get_cfg()
    itr = get_iteration()
    assert cfg is not None
    assert itr is not None
    return cfg, itr


def get_path(name, suffix, mkdir=True):
    cfg, itr = get_cfg_itr_strict()
    path = (cfg.log_dir / "artifact" / name / f"{itr:06d}").with_suffix(suffix)
    if mkdir:
        path.parent.mkdir(parents=True, exist_ok=True)
    return path


def save_fig(name):
    path = get_path(name, "png")
    plt.savefig(path)
    plt.close()
    print(path, "saved.")


def save_wav(name, wav, sr):
    # Lazy import
    import soundfile

    path = get_path(name, ".wav")
    soundfile.write(str(path), wav, sr)
    print(path, "saved.")


def save_tsne(name, x: list, y: list | None = None, m: list[str] | None = None):
    """
    Args:
        x: list of vectors.
        y: list of labels.
        m: list of markers.
    """
    # Lazy import
    from sklearn.manifold import TSNE

    tsne = TSNE(n_components=2)

    x = tsne.fit_transform(x)

    groups = defaultdict(list)

    z = [None] * len(x)

    for xi, yi, ci in zip(x, y or z, m or z):
        groups[yi].append([xi, ci])

    for yi, (xi, ci) in groups.items():
        plt.scatter(*zip(*xi), marker=m, alpha=0.5, y=yi)

    plt.legend()

    save_fig(name)