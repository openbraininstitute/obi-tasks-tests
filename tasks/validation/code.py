import os
import sys
from functools import partial

from entitysdk import Client, models
from entitysdk.token_manager import TokenFromFunction
from obi_auth import get_token


def validate_morphology(client, entity_id) -> dict:
    morphology = client.get_entity(entity_type=models.CellMorphology, entity_id=entity_id)
    assert morphology.type == "cell_morphology"
    return {"entity_id": str(morphology.id)}


if __name__ == "__main__":
    entity_id = sys.argv[1]

    deployment = os.environ["DEPLOYMENT"]
    persistent_token_id = os.environ["PERSISTENT_TOKEN_ID"]

    token_manager = TokenFromFunction(
        partial(
            get_token,
            environment=deployment,
            auth_mode="persistent_token",
            persistent_token_id=persistent_token_id,
        ),
    )

    client = Client(environment="staging", token_manager=token_manager)

    res = validate_morphology(client, entity_id)
    print(f"Success! {res}")
