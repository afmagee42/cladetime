# mypy: ignore-errors

from dataclasses import InitVar, asdict, dataclass, field
from datetime import datetime
from pprint import pprint

from cloudpathlib import AnyPath


@dataclass
class Config:
    sequence_released_date: InitVar[datetime]
    tree_as_of_date: InitVar[datetime]
    data_path_root: InitVar[str] = AnyPath(".")
    sequence_released_since_date: str = None
    reference_tree_date: str = None
    now = datetime.now()
    run_time = now.strftime("%Y%m%dT%H%M%S")
    ncbi_base_url: str = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/virus/genome/download"
    ncbi_package_name: str = "ncbi.zip"
    ncbi_sequence_file: AnyPath = None
    ncbi_sequence_metadata_file: AnyPath = None
    nextstrain_ncov_bucket = "nextstrain-data"
    nextstrain_genome_metadata_key = "files/ncov/open/metadata.tsv.zst"
    nextclade_base_url: str = "https://nextstrain.org/nextclade/sars-cov-2"
    reference_tree_file: AnyPath = None
    root_sequence_file: AnyPath = None
    assignment_no_metadata_file: AnyPath = None
    assignment_file: AnyPath = None
    assignment_file_columns: list[str] = field(default_factory=list)

    def __post_init__(
        self,
        sequence_released_date: datetime,
        tree_as_of_date: datetime,
        data_path_root: str | None,
    ):
        if data_path_root:
            self.data_path = AnyPath(data_path_root)
        else:
            self.data_path = AnyPath(".").home() / "covid_variant" / self.run_time
        self.sequence_released_since_date = sequence_released_date.strftime("%Y-%m-%d")
        self.reference_tree_date = tree_as_of_date.strftime("%Y-%m-%d")
        self.ncbi_sequence_file = self.data_path / "ncbi_dataset/data/genomic.fna"
        self.ncbi_sequence_metadata_file = self.data_path / f"{self.sequence_released_since_date}-metadata.tsv"
        self.reference_tree_file = self.data_path / f"{self.reference_tree_date}_tree.json"
        self.root_sequence_file = self.data_path / f"{self.reference_tree_date}_root_sequence.fasta"
        self.assignment_no_metadata_file = (
            self.data_path / f"{self.sequence_released_since_date}_clade_assignments_no_metadata.csv"
        )
        self.assignment_file = self.data_path / f"{self.sequence_released_since_date}_clade_assignments.csv"
        self.assignment_file_columns = [
            "Accession",
            "Source database",
            "Release date",
            "Update date",
            "Isolate Collection date",
            "clade",
            "clade_nextstrain",
            "Nextclade_pango",
            "partiallyAliased",
            "clade_who",
            "clade_display",
            "Virus Pangolin Classification",
        ]

    def __repr__(self):
        return str(pprint(asdict(self)))
