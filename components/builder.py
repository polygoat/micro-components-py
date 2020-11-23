#!/usr/bin/env python3

import os
import sys
import stat
from colorama import init as colorama_init, Fore, Style
import pydash as _
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(REPO_DIR))

from utils.classes.Component import Component

colorama_init(autoreset=True)

MAPPING = {
	'js': 'node',
	'javascript': 'node',
	'py': 'python'
}

ENDINGS = {
	'python': 'py',
	'node': 'js'
}

class Builder(Component):
	name = 'builder'

	def create(component_name, coding_language='node'):
		data = {
			'name': _.snakeCase(component_name),
			'class_name': _.startCase(_.camelCase(component_name)).replace(' ', ''),
			'cwd': os.getcwd()
		}
		coding_language = _.get(MAPPING, coding_language, coding_language)
		with open(__dirname + f'/../{coding_language}.component', 'r') as template_file:
			render = _.template(template_file.read())
		
		file = render(data)
		file_ending = ENDINGS[coding_language]
		file_path = f'./{data.name}.{file_ending}'

		with open(file_path, 'w') as component_file:
			component_file.write(file)
		
		os.chmod(file_path, 0o775)

		print(Fore.GREEN + ' Component created.' + Style.RESET_ALL + ' Try it by running ' + Fore.YELLOW + f'{file_path} help');

Builder.export_as_cli()