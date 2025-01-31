from numpy import compress
from data import PaperDB
from tqdm import tqdm
import model


class Compressor:
    def __init__(self, source: str, model: model.CompressorModel):
        self._source = source
        self._db = PaperDB()
        self._model = model

    def retrieve(self):
        return self._db.get_papers_for_source(self._source)

    def compress(self):
        df = self.retrieve()
        results = []
        for pid, paper in tqdm(df.iterrows(), total=len(df)):
            title = paper.title
            url = paper.url
            abstract = paper.abstract
            compressed_abstract = self._model.go(abstract)
            self._db.add_abstract_compression(pid, compressed_abstract)
            self._db.commit()
            results.append((title, url, compressed_abstract))


class ArxivCompressor(Compressor):
    def __init__(self, model):
        super().__init__("arxiv", model)

    def retrieve(self):
        df = super().retrieve()
        # Summarise the latest results from arxiv.
        latest_date = max(df.date_published.values)
        print(f"Summarising for date: {latest_date}")
        return df.loc[df.date_published == latest_date]
