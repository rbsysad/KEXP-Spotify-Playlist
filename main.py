from remove_duplicates import RemoveDuplicates
from get_KEXP_data import GetKEXPData
from find_tracks import FindTracks

a = GetKEXPData()
a.parse_results(a.get_results())
a.write_to_playlist()

b = RemoveDuplicates()
b.dedupe()
b.write_to_playlist()

c = FindTracks()
c.call_refresh()
c.import_json()
c.add_to_playlist()