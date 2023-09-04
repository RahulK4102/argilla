#  Copyright 2021-present, the Recognai S.L. team.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from typing import Optional

import typer

from argilla.tasks.callback import init_callback
from argilla.tasks.datasets.delete import delete_dataset
from argilla.tasks.datasets.list import list_datasets
from argilla.tasks.datasets.push import push_to_huggingface

_COMMANDS_REQUIRING_DATASET = ["delete", "push-to-huggingface"]


def callback(
    ctx: typer.Context,
    name: Optional[str] = typer.Option(None, help="The name of the `FeedbackDataset` to which apply the command"),
    workspace: Optional[str] = typer.Option(None, help="The name of the workspace where the `FeedbackDataset` belongs"),
) -> None:
    init_callback()

    from argilla.client.feedback.dataset.local import FeedbackDataset

    if ctx.invoked_subcommand not in _COMMANDS_REQUIRING_DATASET:
        return

    if name is None:
        raise typer.BadParameter("The command requires a workspace name provided using '--name' option")

    try:
        typer.echo(
            f"Retrieving `FeedbackDataset` with name={name} from Argilla..."
            if not workspace
            else f"Retrieving `FeedbackDataset` with name={name} and workspace={workspace} from Argilla..."
        )
        dataset = FeedbackDataset.from_argilla(name=name, workspace=workspace)
    except ValueError as e:
        typer.echo(
            f"`FeedbackDataset` with name={name} not found in Argilla."
            if not workspace
            else f"`FeedbackDataset with name={name} and workspace={workspace} not found in Argilla."
        )
        raise typer.Exit(1) from e
    except Exception as e:
        typer.echo("An unexpected error occurred when trying to get the `FeedbackDataset` from Argilla.")
        raise typer.Exit(code=1) from e

    ctx.obj = dataset


app = typer.Typer(help="Holds CLI commands for datasets management", invoke_without_command=False, callback=callback)

app.command(name="list", help="List datasets linked to user's workspaces")(list_datasets)
app.command(name="push-to-huggingface", help="Push a dataset to HuggingFace Hub")(push_to_huggingface)
app.command(name="delete", help="Deletes a dataset")(delete_dataset)


if __name__ == "__main__":
    app()
