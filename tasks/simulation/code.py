import os
import shutil
import subprocess
from pathlib import Path
import tempfile


NEURODAMUS_DIR = "/tmp/neurodamus"


if __name__ == "__main__":
    neurodamus_python = os.environ["NEURODAMUS_PYTHON"]
    models_dir = Path(os.environ["NEURODAMUS_MODELS"])

    readonly_usecase = f"{NEURODAMUS_DIR}/tests/simulations/usecase3"

    hoc_library_path = models_dir / "share/neurodamus_neocortex/hoc"
    path = f"{models_dir / 'bin'}:{os.environ['PATH']}"

    with tempfile.TemporaryDirectory() as tdir:
        shutil.copytree(readonly_usecase, tdir, dirs_exist_ok=True)

        subprocess.run(
            [
                "mpirun",
                "--use-hwthread-cpus",
                "-np",
                "2",
                "special",
                "-mpi",
                "-python",
                f"{neurodamus_python}/init.py",
                "--configFile=simulation_sonata.json",
            ],
            cwd=tdir,
            check=True,
            env=os.environ
            | {
                "HOC_LIBRARY_PATH": str(hoc_library_path),
                "NRNMECH_LIB_PATH": str(models_dir / "lib/libnrnmech.so"),
                "PATH": path,
            },
        )

        for f in Path(f"{tdir}/reporting").glob("*.h5"):
            print(f)

        subprocess.run(
            [
                "mpirun",
                "--use-hwthread-cpus",
                "-np",
                "2",
                "special",
                "-mpi",
                "-python",
                f"{neurodamus_python}/init.py",
                "--configFile=simulation_sonata_coreneuron.json",
            ],
            cwd=tdir,
            check=True,
            env=os.environ
            | {
                "HOC_LIBRARY_PATH": str(hoc_library_path),
                "CORENEURONLIB": str(models_dir / "lib/libcorenrnmech.so"),
                "PATH": path,
            },
        )

        for f in Path(f"{tdir}/reporting_coreneuron").glob("*.h5"):
            print(f)
