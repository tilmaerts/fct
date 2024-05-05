
.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'



full: ## make the full documentation 
	pdflatex full

bib: ## translate labels to bibtex 
	fct_csvbib *labels.csv

timeline: ## plot the timeline
	fct_timeline timeline.yml tl.png

brief: ## make the brief 
	pdflatex brief 
	biber brief 
	pdflatex brief 

all: full bib brief  ## all 