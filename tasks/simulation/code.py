import subprocess
from pathlib import Path


NEURODAMUS_DIR = "/tmp/neurodamus"


if __name__ == "__main__":
    neurodamus_python = os.environ["NEURODAMUS_PYTHON"]

    subprocess.run(
        [
            "mpirun",
            "--allow-run-as-root",
            "--use-hwthread-cpus",
            "-np",
            "2",
            "special",
            "-mpi",
            "-python",
            f"{neurodamus_python}/init.py",
            "--configFile=simulation_sonata.json",
        ],
        cwd=NEURODAMUS_DIR,
        check=True,
    )

    for f in Path("reporting").glob("*.h5"):
        print(f)

    subprocess.run(
        [
            "mpirun",
            "--allow-run-as-root",
            "--use-hwthread-cpus",
            "-np",
            "2",
            "special",
            "-mpi",
            "-python",
            f"{neurodamus}/init.py",
            "--configFile=simulation_sonata_coreneuron.json",
        ],
        cwd=NEURODAMUS_DIR,
        check=True,
    )

    for f in Path("reporting_coreneuron").glob("*.h5"):
        print(f)
