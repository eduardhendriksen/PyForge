
$PyForgePath = Join-Path $PSScriptRoot "PyForge"
$docsPath = Join-Path $PSScriptRoot "docs"
$falseDocsPaths = Join-Path $DocsPath "PyForge"

pdoc $PyForgePath --html --force -o $DocsPath

get-childitem -path $docsPath -filter *.html | remove-item
get-childitem -path $falseDocsPaths -filter *.html | ForEach-Object {copy-item $_.FullName -filter *.html -Destination $docsPath}
remove-item $falseDocsPaths -recurse
