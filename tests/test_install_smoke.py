from __future__ import annotations

import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallSmokeTest(unittest.TestCase):
    def test_release_zip_is_flat_and_installable(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            package = work / "package"
            for name in (
                "SKILL.md",
                "agents",
                "sellersprite-bi-market-research",
                "requirements.txt",
                "LICENSE",
                ".well-known",
                "PUBLISHER_PUBLIC_KEY.pem",
                "PUBLIC_MANIFEST.sha256",
                "RELEASE_PROVENANCE.json",
                "RELEASE_PROVENANCE.sig",
            ):
                source = ROOT / name
                target = package / name
                if source.is_dir():
                    shutil.copytree(source, target)
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, target)

            archive = work / "skill.zip"
            with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
                for path in package.rglob("*"):
                    if path.is_file():
                        handle.write(path, path.relative_to(package).as_posix())

            extracted = work / "extracted"
            with zipfile.ZipFile(archive) as handle:
                handle.extractall(extracted)

            self.assertTrue((extracted / "SKILL.md").is_file())
            self.assertTrue((extracted / "agents/openai.yaml").is_file())
            self.assertTrue((extracted / "sellersprite-bi-market-research/SKILL.md").is_file())
            self.assertEqual(1, len(list(extracted.glob("SKILL.md"))))
            self.assertEqual(1, len(list(extracted.glob("sellersprite-bi-market-research/SKILL.md"))))
            self.assertFalse((extracted / "sellersprite-bi-market-research/sellersprite-bi-market-research").exists())
            self.assertFalse((extracted / "sellersprite-amazon-market-research-bi-skill").exists())


if __name__ == "__main__":
    unittest.main()
