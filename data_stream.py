from typing import Any
from data_processor import (
    DataProcessor,
    NumericProcessor,
    TextProcessor,
    LogProcessor,
)


class DataStream:

    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            processed = False
            for proc in self.processors:
                if proc.validate(item):
                    proc.ingest(item)
                    processed = True
                    break
            if not processed:
                print(
                    "DataStream error - "
                    f"Can't process element in stream: {item}"
                )

    def print_processors_stats(self) -> None:
        if not self.processors:
            print("== DataStream statistics ==\nNo processor found, no data")
            return

        print("== DataStream statistics ==")
        for proc in self.processors:
            name = proc.__class__.__name__
            readable_name = name.replace("Processor", " Processor")
            print(
                f"{readable_name.strip()}: "
                f"total {proc.total_processed} items processed, "
                f"remaining {proc.remaining_count} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("Initialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("Registering Numeric Processor")
    num_proc = NumericProcessor()
    stream.register_processor(num_proc)

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

    print("Registering other data processors")
    txt_proc = TextProcessor()
    log_proc = LogProcessor()
    stream.register_processor(txt_proc)
    stream.register_processor(log_proc)

    print("Send the same batch again")
    stream.process_stream(batch1)

    stream.print_processors_stats()

    print(
        "Consume some elements from the data "
        "processors: Numeric 3, Text 2, Log 1"
    )
    for _ in range(3):
        if num_proc.remaining_count > 0:
            num_proc.output()
    for _ in range(2):
        if txt_proc.remaining_count > 0:
            txt_proc.output()
    for _ in range(1):
        if log_proc.remaining_count > 0:
            log_proc.output()

    stream.print_processors_stats()

    print(
        "\nHow does polymorphism allow the DataStream to handle "
        "different data types in the stream without knowing "
        "their specific implementations?"
    )
    print(
        "Polymorphism allows DataStream to interact with any "
        "DataProcessor through a common interface (validate and ingest). "
        "DataStream delegates compatibility checking and ingestion "
        "to the specific processor instance without needing "
        "conditional type checks."
    )
    print("What are the benefits of this design approach?")
    print(
        "It promotes high cohesion and low coupling, adhering to the "
        "Open-Closed Principle where new processors can be added "
        "without modifying core stream logic."
    )


if __name__ == "__main__":
    main()
