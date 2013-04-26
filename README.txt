Gnacs
=====

Gnip normalized activities parser

Install with,
pip install diacs



diacs.py takes 0 or more arguments and reads 1 or more JSON disqus
activities from standard input.  The activities are parsed and 
output is pipe-delimited records representing a subset of the activity
fields.

$ ./gnacs.py -h
Usage: gnacs.py [options]

Options:
  -h, --help            show this help message and exit
  -g, --geo             Include geo fields
  -i, --influence       Show user's influence metrics
  -c, --csv             Comma-delimited output (default is | without quotes)
  -l, --lang            Include language fields
  -p, --pretty          Pretty JSON output of full records
  -s, --urls            Include urls fields
  -t, --structure       Include thread linking fields
  -r, --rules           Include rules fields
  -u, --user            Include user fields
  -x, --explain         Show field names in output for for sample input
                        records
  -z PUB, --publisher=PUB
                        Publisher(default is twitter)  twitter, disqus,
                        wordpress, wpcomments
