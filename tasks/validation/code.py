import logging
import os
import sys
from functools import partial
from pathlib import Path

from entitysdk import Client, models
from entitysdk.token_manager import TokenFromFunction
from obi_auth import get_token


def validate_morphology(client, entity_id) -> dict:
    morphology = client.get_entity(
        entity_type=models.CellMorphology, entity_id=entity_id
    )
    assert morphology.type == "cell_morphology"
    return {"entity_id": str(morphology.id)}


def ls(path):
    p = Path(path)
    if not p.exists():
        print(f"{path} does not exist")
        return
    for directory in sorted(p.rglob("*")):
        if directory.is_dir():
            print(f"{directory}:")
            for f in sorted(directory.iterdir()):
                if f.is_file():
                    s = f.stat()
                    print(f"  {oct(s.st_mode)[-3:]}  {s.st_size:>10}  {f.name}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )
    ls("/data/aws_s3_internal/private")

    entity_id = sys.argv[1]

    deployment = os.environ["DEPLOYMENT"]
    persistent_token_id = os.environ["PERSISTENT_TOKEN_ID"]

    print(f"{deployment=}")

    token_manager = TokenFromFunction(
        partial(
            get_token,
            environment=deployment,
            auth_mode="persistent_token",
            persistent_token_id=persistent_token_id,
        ),
    )

    client = Client(environment=deployment, token_manager=token_manager)

    res = validate_morphology(client, entity_id)
    print(f"Success! {res}")
