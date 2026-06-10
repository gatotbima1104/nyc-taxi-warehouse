from pathlib import Path

class Helper:
    @staticmethod
    def create_dir(output_path: Path) -> Path:
        """
            Make a directory with pathlib
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return output_path.parent