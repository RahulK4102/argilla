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

from typing import List

from argilla.tasks import async_typer


def list_workspaces() -> None:
    """List the workspaces in Argilla and prints them on the console."""
    from rich.console import Console
    from rich.table import Table

    from argilla import Workspace

    workspaces = Workspace.list()

    table = Table(title="Workspaces")
    for column in ("ID", "Name", "Creation Date", "Update Date"):
        table.add_column(column, justify="center")

    for workspace in workspaces:
        table.add_row(
            str(workspace.id),
            workspace.name,
            workspace.inserted_at.isoformat(sep=" "),
            workspace.updated_at.isoformat(sep=" "),
        )

    console = Console()
    console.print(table)


if __name__ == "__main__":
    async_typer.run(list_workspaces)