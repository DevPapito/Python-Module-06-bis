from typing import Protocol
from data_processor import LogProcessor, NumericProcessor, TextProcessor
from data_stream import DataStream as BaseDataStream


class ExportPlugin(Protocol):

    def process_output(self, data: list[tuple[int, str]]) -> None:
        ...


class CSVExportPlugin:

    def process_output(self, data: list[tuple[int, str]]) -> None:
        values = [val for _, val in data]
        print("CSV Output:")
        print(",".join(values))


class JSONExportPlugin:

    def process_output(self, data: list[tuple[int, str]]) -> None:
        print("JSON Output:")
        items = []
        for rank, val in data:
            items.append(f'"item_{rank}": "{val}"')
        print("{" + ", ".join(items) + "}")


class DataStream(BaseDataStream):

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            collected: list[tuple[int, str]] = []
            for _ in range(nb):
                if proc.remaining_count > 0:
                    collected.append(proc.output())
            if collected:
                plugin.process_output(collected)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Processors")
    num_proc = NumericProcessor()
    txt_proc = TextProcessor()
    log_proc = LogProcessor()
    stream.register_processor(num_proc)
    stream.register_processor(txt_proc)
    stream.register_processor(log_proc)

    batch1 = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead",
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected",
            },
        ],
        42,
        ["Hi", "five"],
    ]
    print(f"Send first batch of data on stream: {batch1}")
    stream.process_stream(batch1)
    stream.print_processors_stats()

    print("Send 3 processed data from each processor to a CSV plugin:")
    csv_plugin = CSVExportPlugin()
    stream.output_pipeline(3, csv_plugin)

    stream.print_processors_stats()

    batch2 = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash",
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days",
            },
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
    print(f"Send another batch of data: {batch2}")
    stream.process_stream(batch2)
    stream.print_processors_stats()

    print("Send 5 processed data from each processor to a JSON plugin:")
    json_plugin = JSONExportPlugin()
    stream.output_pipeline(5, json_plugin)

    stream.print_processors_stats()

    print(
        "\nDataProcessor is an ABC and ExportPlugin is a Protocol. "
        "Both constrain what a class must provide. What is the actual "
        "difference, and why does a plugin system want the second one?"
    )
    print(
        "An Abstract Base Class (ABC) enforces nominal subtyping "
        "(inheritance), whereas a Protocol enforces structural typing "
        "(duck typing). Plugin systems prefer Protocols because "
        "third-party or external classes can act as plugins without "
        "inheriting from a specific base class."
    )


if __name__ == "__main__":
    main()
