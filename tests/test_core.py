KEY='elements'
import unittest, json, tempfile, copy
from pathlib import Path
from core import validate, analyze
from server import Store, Conflict
SAMPLE=json.loads((Path(__file__).resolve().parents[1]/"examples/sample.json").read_text())
class Tests(unittest.TestCase):
    def fresh(self):return copy.deepcopy(SAMPLE)
    def test_sample_roundtrip(self):
        doc=validate(self.fresh());self.assertEqual(doc,validate(json.loads(json.dumps(doc))));self.assertTrue(analyze(doc)["metrics"])
    def test_invalid_version(self):
        for version in [True,2,"1",None]:
            d=self.fresh();d["version"]=version
            with self.assertRaises(ValueError):validate(d)
    def test_duplicate_identity(self):
        d=self.fresh();d[KEY].append(copy.deepcopy(d[KEY][0]))
        with self.assertRaises(ValueError):validate(d)
    def test_empty_document(self):
        d=self.fresh();d[KEY]=[];self.assertEqual(validate(d)[KEY],[]);analyze(validate(d))
    def test_oversized_collection(self):
        d=self.fresh();d[KEY]=[dict(d[KEY][0],id="x"+str(i)) for i in range(151)]
        with self.assertRaises(ValueError):validate(d)
    def test_storage_revision_and_reopen(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"library.sqlite3";store=Store(path)
            first=store.save({"revision":0,"document":self.fresh()});second=store.save({**first,"document":dict(first["document"],title="Changed")})
            self.assertEqual(second["revision"],2)
            with self.assertRaises(Conflict):store.save(first)
            self.assertEqual(Store(path).get(first["id"])["document"]["title"],"Changed")
    def test_invalid_save_preserves_previous(self):
        with tempfile.TemporaryDirectory() as tmp:
            store=Store(Path(tmp)/"library.sqlite3");first=store.save({"revision":0,"document":self.fresh()})
            with self.assertRaises(ValueError):store.save({**first,"document":{"version":2}})
            self.assertEqual(store.get(first["id"]),first)
    def test_empty_document_id_does_not_create_duplicate(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp) / "library.sqlite3")
            first = store.save({"revision": 0, "document": self.fresh()})
            library = store.list()
            with self.assertRaisesRegex(ValueError, "Invalid document ID"):
                store.save({**first, "id": "", "revision": 0})
            self.assertEqual(store.list(), library)
            self.assertEqual(store.get(first["id"]), first)
            document = dict(first["document"], title="Updated title")
            saved = store.save({**first, "document": document})
            self.assertEqual(saved["id"], first["id"])
            self.assertEqual(saved["revision"], 2)
            self.assertEqual(store.get(first["id"])["document"], document)
            self.assertEqual(len(store.list()), 1)
    def test_out_of_bounds_rejected(self):
        d=self.fresh();d["elements"][0]["x"]=200
        with self.assertRaises(ValueError):validate(d)
    def test_css_values_rejected(self):
        for value in ["red","url(x)","#ffffff; display:none"]:
            d=self.fresh();d["elements"][0]["color"]=value
            with self.assertRaises(ValueError):validate(d)
    def test_layer_order_preserved(self):
        d=self.fresh();d["elements"].reverse();self.assertEqual(validate(d)["elements"],d["elements"])
    def test_overflow_is_notice(self):
        d=self.fresh();d["elements"][1]["text"]="Long line "*20
        self.assertIn("title",analyze(validate(d))["overflow"])
    def test_non_string_layer_text_preserves_saved_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp) / "library.sqlite3")
            first = store.save({"revision": 0, "document": self.fresh()})
            for value in [None, False, True, 0, 1, [], {}, ["text"]]:
                with self.subTest(value=value):
                    document = copy.deepcopy(first["document"])
                    document["elements"][1]["text"] = value
                    with self.assertRaisesRegex(ValueError, "Layer text must be a string"):
                        store.save({**first, "document": document})
                    self.assertEqual(store.get(first["id"]), first)
            document = copy.deepcopy(first["document"])
            document["elements"][1]["text"] = "Valid replacement"
            saved = store.save({**first, "document": document})
            self.assertEqual(saved["revision"], 2)
            self.assertEqual(store.get(first["id"])["document"], document)

    def test_empty_and_missing_layer_text_keep_placeholder(self):
        for missing in [False, True]:
            with self.subTest(missing=missing):
                document = self.fresh()
                if missing:
                    del document["elements"][1]["text"]
                else:
                    document["elements"][1]["text"] = ""
                self.assertEqual(validate(document)["elements"][1]["text"], "—")

    def test_locked_type(self):
        d=self.fresh();d["elements"][0]["locked"]="yes"
        with self.assertRaises(ValueError):validate(d)

if __name__=="__main__":unittest.main()
