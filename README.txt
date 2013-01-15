diacs
=====

Gnip normalized Disqus activities parser

Install with,
pip install diacs

diacs.py takes 0 or more arguments and reads 1 or more JSON disqus
activities from standard input.  The activities are parsed and 
output is pipe-delimited records representing a subset of the activity
fields.


Usage: diacs.py [options]

Options:
  -h, --help    show this help message and exit
  -u, --user    Include user fields
  -r, --rules   Include rules fields
  -s, --structure    Include thread structure fields
  -l, --lang    Include language fields
  -p, --pretty  Pretty JSON output of full records

For example, to parse activites from file disqus_data.json,

    cat disqus_data.json | diacs.py > disqus.piped
