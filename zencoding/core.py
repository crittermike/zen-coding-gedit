#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Core Zen Coding library. Contains various text manipulation functions:

== Expand abbreviation
Expands abbreviation like ul#nav>li*5>a into a XHTML string.

=== How to use
First, you have to extract current string (where cursor is) from your test
editor and use <code>find_abbr_in_line()</code> method to extract abbreviation.
If abbreviation was found, this method will return it as well as position index
of abbreviation inside current line. If abbreviation wasn't found, method
returns empty string. With abbreviation found, you should call
<code>parse_into_tree()</code> method to transform abbreviation into a tag tree.
This method returns <code>Tag</code> object on success, None on failure. Then
simply call <code>to_string()</code> method of returned <code>Tag</code> object
to transoform tree into a XHTML string

You can setup output profile using <code>setup_profile()</code> method
(see <code>default_profile</code> definition for available options)

Created on Apr 17, 2009

@author: Sergey Chikuyonok (http://chikuyonok.ru)
'''
from settings import zen_settings
import re
import parser

newline = '\n'
"Newline symbol"

insertion_point = '|'
"Symbol which refers to cursor position"

sub_insertion_point = '|'
"""@deprecated: Symbol which refers to cursor position (for editors which support multiple placeholders)"""

content_placeholder = '{%::zen-content::%}'

re_tag = re.compile(r'<\/?[\w:\-]+(?:\s+[\w\-:]+(?:\s*=\s*(?:(?:"[^"]*")|(?:\'[^\']*\')|[^>\s]+))?)*\s*(\/?)>$')

profiles = {}

default_profile = {
	'tag_case': 'lower',         # values are 'lower', 'upper'
	'attr_case': 'lower',        # values are 'lower', 'upper'
	'attr_quotes': 'double',     # values are 'single', 'double'

	'tag_nl': 'decide',          # each tag on new line, values are True, False, 'decide'

	'place_cursor': True,        # place cursor char "| (pipe)" in output

	'indent': True,              # indent tags

	'self_closing_tag': 'xhtml'  # use self-closing style for writing empty elements, e.g. <br /> or <br>.
                                 # values are True, False, 'xhtml'
}

def has_deep_key(obj, key):
	"""
	Check if <code>obj</code> dictionary contains deep key. For example,
	example, it will allow you to test existance of my_dict[key1][key2][key3],
	testing existance of my_dict[key1] first, then my_dict[key1][key2],
	and finally my_dict[key1][key2][key3]
	@param obj: Dictionary to test
	@param obj: dict
	@param key: Deep key to test. Can be list (like ['key1', 'key2', 'key3']) or
	string (like 'key1.key2.key3')
	@type key: list, tuple, str
	@return: bool
	"""
	if isinstance(key, str):
		key = key.split('.')

	last_obj = obj
	for v in key:
		if not last_obj.has_key(v):
			return False
		last_obj = last_obj[v]

	return True


def is_allowed_char(ch):
	"""
	Test if passed symbol is allowed in abbreviation
	@param ch: Symbol to test
	@type ch: str
	@return: bool
	"""
	return ch.isalnum() or ch in "#.>+*:$-_!@"

def split_by_lines(text, remove_empty=False):
	"""
	Split text into lines. Set <code>remove_empty</code> to true to filter out
	empty lines
	@param text: str
	@param remove_empty: bool
	@return list
	"""
	lines = text.splitlines()

	return remove_empty and [line for line in lines if line.strip()] or lines

def make_map(prop):
	"""
	Helper function that transforms string into dictionary for faster search
	@param prop: Key name in <code>zen_settings['html']</code> dictionary
	@type prop: str
	"""
	obj = {}
	for a in zen_settings['html'][prop].split(','):
		obj[a] = True

	zen_settings['html'][prop] = obj

def create_profile(options):
	"""
	Create profile by adding default values for passed optoin set
	@param options: Profile options
	@type options: dict
	"""
	for k, v in default_profile.items():
		options.setdefault(k, v)

	return options

def setup_profile(name, options = {}):
	"""
	@param name: Profile name
	@type name: str
	@param options: Profile options
	@type options: dict
	"""
	profiles[name.lower()] = create_profile(options);

def get_newline():
	"""
	Returns newline symbol which is used in editor. This function must be
	redefined to return current editor's settings
	@return: str
	"""
	return newline

def string_to_hash(text):
	"""
	Helper function that transforms string into hash
	@return: dict
	"""
	obj = {}
	items = text.split(",")
	for i in items:
		obj[i] = True

	return obj

def pad_string(text, pad):
	"""
	Indents string with space characters (whitespace or tab)
	@param text: Text to indent
	@type text: str
	@param pad: Indentation level (number) or indentation itself (string)
	@type pad: int, str
	@return: str
	"""
	pad_str = ''
	result = ''
	if (type(pad) is int):
		pad_str = zen_settings['variables']['indentation'] * pad
	else:
		pad_str = pad

	nl = get_newline()
	lines = text.split(nl)
	result = result + lines[0]
	for line in lines[1:]:
		result += nl + pad_str + line

	return result

def is_snippet(abbr, doc_type = 'html'):
	"""
	Check is passed abbreviation is a snippet
	@return bool
	"""
	return get_snippet(doc_type, abbr) and True or False

def is_ends_with_tag(text):
	"""
	Test is string ends with XHTML tag. This function used for testing if '<'
	symbol belogs to tag or abbreviation
	@type text: str
	@return: bool
	"""
	return re_tag.search(text) != None

def get_elements_collection(resource, type):
	"""
	Returns specified elements collection (like 'empty', 'block_level') from
	<code>resource</code>. If collections wasn't found, returns empty object
	@type resource: dict
	@type type: str
	@return: dict
	"""
	if 'element_types' in resource and type in resource['element_types']:
		return resource['element_types'][type]
	else:
		return {}

def replace_variables(text, vars=zen_settings['variables']):
	"""
	Replace variables like ${var} in string
	@param text: str
	@return: str
	"""
	return re.sub(r'\$\{([\w\-]+)\}', lambda m: m.group(1) in vars and vars[m.group(1)] or m.group(0), text)

def get_abbreviation(res_type, abbr):
	"""
	Returns abbreviation value from data set
	@param res_type: Resource type (html, css, ...)
	@type res_type: str
	@param abbr: Abbreviation name
	@type abbr: str
	@return dict, None
	"""
	return get_settings_resource(res_type, abbr, 'abbreviations')

def get_snippet(res_type, snippet_name):
	"""
	Returns snippet value from data set
	@param res_type: Resource type (html, css, ...)
	@type res_type: str
	@param snippet_name: Snippet name
	@type snippet_name: str
	@return dict, None
	"""
	return get_settings_resource(res_type, snippet_name, 'snippets');

def get_settings_resource(res_type, abbr, res_name):
	"""
	Returns resurce value from data set with respect of inheritance
	@param res_type: Resource type (html, css, ...)
	@type res_type: str
	@param abbr: Abbreviation name
	@type abbr: str
	@param res_name: Resource name ('snippets' or 'abbreviation')
	@type res_name: str
	@return dict, None
	"""

	if zen_settings.has_key(res_type):
		resource = zen_settings[res_type];
		if (has_deep_key(resource, [res_name, abbr])):
			return resource[res_name][abbr]
		elif 'extends' in resource:
	#		find abbreviation in ancestors
			for v in resource['extends']:
				if has_deep_key(zen_settings, [v, res_name, abbr]):
					return zen_settings[v][res_name][abbr]
	return None;


def parse_into_tree(abbr, doc_type='html'):
	"""
	Transforms abbreviation into a simple element's tree
	@param abbr: Abbreviation to transform
	@type abbr: str
	@param doc_type: Document type (xsl, html), a key of dictionary where to
	search abbreviation settings
	@type doc_type: str
	@return: Tag
	"""
	root = Tag('', 1, doc_type)
	token = re.compile(r'([\+>])?([a-z@\!][a-z0-9:\-]*)(#[\w\-\$]+)?((?:\.[\w\-\$]+)*)(\*(\d*))?(\+$)?', re.IGNORECASE)

	if not abbr:
		return None

	def expando_replace(m):
		ex = m.group(0)
		a = get_abbreviation(doc_type, ex)
		return a and a.value or ex

	def token_expander(operator, tag_name, id_attr, class_name, has_multiplier, multiplier, has_expando):

		multiply_by_lines = (has_multiplier and not multiplier)
		multiplier = multiplier and int(multiplier) or 1

		if has_expando:
			tag_name += '+'

		current = is_snippet(tag_name, doc_type) and Snippet(tag_name, multiplier, doc_type) or Tag(tag_name, multiplier, doc_type)

		if id_attr:
			current.add_attribute('id', id_attr[1:])
		if class_name:
			current.add_attribute('class', class_name[1:].replace('.', ' '))

		# dive into tree
		if operator == '>' and token_expander.last:
			token_expander.parent = token_expander.last;

		token_expander.parent.add_child(current)
		token_expander.last = current

		if multiply_by_lines:
			root.multiply_elem = current

		return ''

	# replace expandos
	abbr = re.sub(r'([a-z][a-z0-9]*)\+$', expando_replace, abbr)

	token_expander.parent = root
	token_expander.last = None


    # abbr = re.sub(token, lambda m: token_expander(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7)), abbr)
	# Issue from Einar Egilsson
	abbr = token.sub(lambda m: token_expander(m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6), m.group(7)), abbr)

	root.last = token_expander.last

	# empty 'abbr' variable means that abbreviation was expanded successfully,
	# non-empty variable means there was a syntax error
	return not abbr and root or None;

def find_abbr_in_line(line, index = 0):
	"""
	Search for abbreviation inside line of code and returns it
	@param line: Line of code
	@type line: str

	@param index: Caret position inside line (where to start searching)
	@type index: int

	@return: str
	"""
	start_index = 0
	cur_index = index - 1
	while cur_index >= 0:
		ch = line[cur_index]
		if not is_allowed_char(ch) or (ch == '>' and is_ends_with_tag(line[0:cur_index + 1])):
			start_index = cur_index + 1
			break
		cur_index = cur_index - 1

	return line[start_index:index], start_index

def expand_abbreviation(abbr, doc_type = 'html', profile_name = 'plain'):
	"""
	Expands abbreviation into a XHTML tag string

	@type abbr: str
	@return: str
	"""
	tree = parse_into_tree(abbr, doc_type)
	if tree:
		return replace_variables(re.sub('\|', insertion_point, tree.to_string(profile_name) or ''))

	return ''

def is_inside_tag(html, cursor_pos):
	re_tag = re.compile(r'^<\/?\w[\w\:\-]*.*?>')

	# search left to find opening brace
	pos = cursor_pos
	while pos > -1:
		if html[pos] == '<': break
		pos -= 1


	if pos != -1:
		m = re_tag.match(html[pos:]);
		if m and cursor_pos > pos and cursor_pos < pos + len(m.group(0)):
			return True

	return False

def wrap_with_abbreviation(abbr, text, doc_type='html', profile='plain'):
	"""
	Wraps passed text with abbreviation. Text will be placed inside last
	expanded element
	@param abbr: Abbreviation
	@type abbr: str

	@param text: Text to wrap
	@type text: str

	@param doc_type: Document type (html, xml, etc.)
	@type doc_type: str

	@param profile: Output profile's name.
	@type profile: str
	@return {String}
	"""
	tree = parse_into_tree(abbr, doc_type)
	if tree:
		repeat_elem = tree.multiply_elem or tree.last
		repeat_elem.set_content(text)
		repeat_elem.repeat_by_lines = bool(tree.multiply_elem)
		return replace_variables(re.sub('\|', insertion_point, tree.to_string(profile) or ''))
	else:
		return None

def update_settings(settings):
	globals()['zen_settings'] = settings

class Tag(object):
	def __init__(self, name, count=1, doc_type='html'):
		"""
		@param name: Tag name
		@type name: str
		@param count:  How many times this tag must be outputted
		@type count: int
		@param doc_type: Document type (xsl, html)
		@type doc_type: str
		"""
		name = name.lower()

		abbr = get_abbreviation(doc_type, name)

		if abbr and abbr.type == parser.TYPE_REFERENCE:
			abbr = get_abbreviation(doc_type, abbr.value)

		self.name = abbr and abbr.value['name'] or name.replace('+', '')
		self.count = count
		self.children = []
		self.attributes = []
		self.multiply_elem = None
		self.__attr_hash = {}
		self.__abbr = abbr
		self.__content = ''
		self.repeat_by_lines = False
		self.__res = zen_settings.has_key(doc_type) and zen_settings[doc_type] or {}

		# add default attributes
		if self.__abbr and 'attributes' in self.__abbr.value:
			for a in self.__abbr.value['attributes']:
				self.add_attribute(a['name'], a['value'])

	def get_content(self):
		return self.__content

	def set_content(self, value):
		self.__content = value

	def add_attribute(self, name, value):
		"""
		Add attribute to tag. If the attribute with the same name already exists,
		it will be overwritten, but if it's name is 'class', it will be merged
		with the existed one
		@param name: Attribute nama
		@type name: str
		@param value: Attribute value
		@type value: str
		"""
		if name in self.__attr_hash:
#			attribue already exists
			a = self.__attr_hash[name]
			if name == 'class':
#				'class' is a magic attribute
				if a['value']:
					value = ' ' + value
				a['value'] += value
			else:
				a['value'] = value
		else:
			a = {'name': name, 'value': value}
			self.__attr_hash[name] = a
			self.attributes.append(a)

	def add_child(self, tag):
		"""
		Add new child
		@param tag: ÐŸÐ¾Ñ‚Ð¾Ð¼Ð¾Ðº
		@type tag: Tag
		"""
		self.children.append(tag)

	def __has_element(self, collection_name, def_value = False):
		if collection_name in self.__res:
			return self.name in self.__res[collection_name]
		else:
			return def_value


	def is_empty(self):
		"""
		Test if current XHTML element is an empty (must not contain any children)
		element
		@return: bool
		"""

		return (self.__abbr and self.__abbr.value['is_empty']) or \
			self.name in get_elements_collection(self.__res, 'empty')

	def is_inline(self):
		"""
		Test if current XHTML element is an inline element
		@return: bool
		"""
		return self.name in get_elements_collection(self.__res, 'inline_level')

	def is_block(self):
		"""
		Test if current element is a block-level element
		@return: bool
		"""
		return self.name in get_elements_collection(self.__res, 'block_level')

	def has_tags_in_content(self):
		"""
		This function tests if current tags' content contains XHTML tags.
	 	This function is mostly used for output formatting
		"""
		return self.get_content() and re_tag.search(self.get_content())


	def has_block_children(self):
		"""
		Test if current tag contains block-level elements. Used for output
		formatting
		@return: bool
		"""
		if self.has_tags_in_content() and self.is_block():
			return True

		for tag in self.children:
			if tag.is_block():
				return True
		return False

	def set_content(self, content): #@DuplicatedSignature
		self.__content = content

	def get_content(self): #@DuplicatedSignature
		return self.__content

	def find_deepest_child(self):
		"""
		Search for deepest and latest child of current element.
		Returns None if there's no children
	 	@return Tag or None
		"""
		if not self.children:
			return None

		deepest_child = self
		while True:
			deepest_child = deepest_child.children[-1]
			if not deepest_child.children:
				break

		return deepest_child

	def output_children(self, profile_name):
		"""
		Output all children as a string
		@type profile_name: str
		@return: str
		"""
		content = ''
		profile = profile_name in profiles and profiles[profile_name] or profiles['plain']
		for tag in self.children:
				content += tag.to_string(profile_name)

				if self.children.index(tag) != len(self.children) - 1 and \
					(profile['tag_nl'] == True or \
					(profile['tag_nl'] == 'decide' and tag.is_block())):
						content += get_newline()
		return content


	def to_string(self, profile_name):
		"""
		Transforms tag into a string using <code>profile_name</code> settings
		@type profile_name: string
		@return: str
		"""

		if profile_name not in profiles:
			profile_name = 'plain'

		result = []
		profile = profiles[profile_name]
		attrs = ''
		content = ''
		start_tag = ''
		end_tag = ''
		attr_quote = profile['attr_quotes'] == 'single' and "'" or '"'
		cursor = profile['place_cursor'] and '|' or ''
		self_closing = ''

		is_empty = self.is_empty() and not self.children


		if profile['self_closing_tag'] == 'xhtml':
			self_closing = ' /'
		elif profile['self_closing_tag'] == True:
			self_closing = '/'

		def allow_newline(tag):
			return (profile['tag_nl'] is True) or (profile['tag_nl'] == 'decide' and tag.is_block())

		# make attribute string
		for a in self.attributes:
			if profile['attr_case'] == 'upper':
				attr_name = a['name'].upper()
			else:
				attr_name = a['name'].lower()

			attrs += ' %s=%s%s%s' % (attr_name, attr_quote, a['value'] or cursor, attr_quote)

		deepest_child = self.find_deepest_child()

		# output children
		if not is_empty:
			if deepest_child and self.repeat_by_lines:
				deepest_child.set_content(content_placeholder)

			for i, child in enumerate(self.children):
				content += child.to_string(profile_name)

				if child != self.children[-1] and \
					(allow_newline(child) or allow_newline(self.children[i + 1])):
					content += get_newline()

		# define opening and closing tags
		if self.name:
			tag_name = profile['tag_case'] == 'upper' and self.name.upper() or self.name.lower()
			if is_empty:
				start_tag = '<%s%s%s>' % (tag_name, attrs, self_closing)
			else:
				start_tag, end_tag = '<%s%s>' % (tag_name, attrs), '</%s>' % tag_name

		# output formatting
		if profile['tag_nl'] != False:
			if self.name and (profile['tag_nl'] == True or self.has_block_children()):
				if not self.is_empty():
					start_tag += get_newline() + zen_settings['variables']['indentation']
					end_tag = get_newline() + end_tag


			if self.name:
				if content:
					content = pad_string(content, profile['indent'] and 1 or 0)
				elif not is_empty:
					start_tag += cursor

		# repeat tag by lines count
		cur_content = ''
		if self.repeat_by_lines:
			lines = split_by_lines(self.get_content().strip(), True)
			for j, line in enumerate(lines):
				if deepest_child: cur_content = ''
				else: cur_content = content_placeholder

				if content and not deepest_child:
					cur_content += get_newline()

				elem_str = start_tag.replace('$', str(j + 1)) + cur_content + content + end_tag
				result.append(elem_str.replace(content_placeholder, line.strip()))

		# repeat tag output
		if not result:
			if self.get_content():
				pad = (profile['tag_nl'] is True or (self.has_tags_in_content() and self.is_block())) and 1 or 0
				content = pad_string(self.get_content(), pad) + content

			for i in range(self.count):
				result.append(start_tag.replace('$', str(i + 1)) + content + end_tag)

		glue = ''
		if allow_newline(self):
			glue = get_newline()

		return glue.join(result)

class Snippet(Tag):
	def __init__(self, name, count=1, doc_type='html'):
		super(Snippet, self).__init__(name, count, doc_type)
		self.value = get_snippet(doc_type, name)
		self.attributes = {'id': '|', 'class': '|'}
		self.__res = zen_settings[doc_type]

	def add_attribute(self, name='', value=''):
		self.attributes[name] = value

	def is_block(self):
		return True

	def to_string(self, profile_name):
		content = ''
		profile = profile_name in profiles and profiles[profile_name] or profiles['plain']
		result = []
		data = self.value
		begin = ''
		end = ''
		child_padding = ''
		child_token = '${child}'
		child_indent = re.compile(r'(^\s+)')

		if data:
			if profile['tag_nl'] != False:
				data = data.replace(r'\n', get_newline())
				# Ð½ÑƒÐ¶Ð½Ð¾ ÑƒÐ·Ð½Ð°Ñ‚ÑŒ, ÐºÐ°ÐºÐ¾Ð¹ Ð¾Ñ‚ÑÑ‚ÑƒÐ¿ Ð´Ð¾Ð»Ð¶ÐµÐ½ Ð±Ñ‹Ñ‚ÑŒ Ñƒ Ð¿Ð¾Ñ‚Ð¾Ð¼ÐºÐ¾Ð²
				for line in data.split(get_newline()):
					if child_token in line:
						m = child_indent.match(line)
						child_padding = m and m.group(1) or ''
						break

			if child_token in data:
				begin, end = data.split(child_token, 1)
			else:
				begin = data

		for child in self.children:
			content += child.to_string(profile_name)
			if child != self.children[-1] and \
				(profile['tag_nl'] == True or \
					(profile['tag_nl'] == 'decide' and child.is_block())):
				content += get_newline();

		if child_padding:
			content = pad_string(content, child_padding)

		# substitute attributes
		begin = replace_variables(begin, self.attributes)
		end = replace_variables(end, self.attributes)

		# fix indentation
		indent = zen_settings['variables']['indentation']
		begin = begin.replace('\\t', indent)
		end = end.replace('\\t', indent)

		if self.get_content():
			content = pad_string(self.get_content(), 1) + content

		# multiply output
		result += [begin + content + end for i in range(self.count)]

		glue = profile['tag_nl'] != False and get_newline() or ''

		return glue.join(result)


# create default profiles
setup_profile('xhtml');
setup_profile('html', {'self_closing_tag': False});
setup_profile('xml', {'self_closing_tag': True, 'tag_nl': True});
setup_profile('plain', {'tag_nl': False, 'indent': False, 'place_cursor': False});

# This method call explicity loads default settings from zen_settings.py on start up
# Comment this line if you want to load data from other resources (like editor's
# native snippet)
update_settings(parser.get_settings())

