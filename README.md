# Archive of UML files from GitHub
Following the [index](http://oss.models-db.com/) mined in 2016, this repo archives the UML files referenced by the index that are still reachable.

The first release of the archive has been mined in May 2021. Only 1.6k of 3k `.xmi` from the index are retrievable. All `.xmi` files are stored using different formats (metamodels) dating back to as early as 2000.

## How to perform another archive extraction
To perform another archive extraction with the index, you need to create a text file called `access_token.txt` where your GitHub access token is stored in plain text. Then run `python download.py UMLFiles_List_V2.0.csv`. This will take a while depending on your Internet connection.