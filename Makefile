.PHONY: run
run:
	python3 main.py
.PHONY: format
format:
	black .
	isort .

.PHONY: help
help:
	@echo "Available targets:"
	@echo " run: Run the script"
	@echo " format: Format the code"
	@echo " help: Show this help message"
