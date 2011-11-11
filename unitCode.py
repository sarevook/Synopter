import re
import xml.sax.handler

def xml2obj(src):
    """
    A simple function to converts XML data into native Python object.
    """

    non_id_char = re.compile('[^_0-9a-zA-Z]')
    def _name_mangle(name):
        return non_id_char.sub('_', name)

    class DataNode(object):
        def __init__(self):
            self._attrs = {}    # XML attributes and child elements
            self.data = None    # child text data
        def __len__(self):
            # treat single element as a list of 1
            return 1
        def __getitem__(self, key):
            if isinstance(key, basestring):
                return self._attrs.get(key,None)
            else:
                return [self][key]
        def __contains__(self, name):
            return self._attrs.has_key(name)
        def __nonzero__(self):
            return bool(self._attrs or self.data)
        def __getattr__(self, name):
            if name.startswith('__'):
                # need to do this for Python special methods???
                raise AttributeError(name)
            return self._attrs.get(name,None)
        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                # multiple attribute of the same name are represented by a list
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value
        def __str__(self):
            return self.data or ''
        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return u'{%s}' % ', '.join([u'%s:%s' % (k,repr(v)) for k,v in items])

    class TreeBuilder(xml.sax.handler.ContentHandler):
        def __init__(self):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []
        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            # xml attributes --> python attributes
            for k, v in attrs.items():
                self.current._add_xml_attr(_name_mangle(k), v)
        def endElement(self, name):
            text = ''.join(self.text_parts).strip()
            if text:
                self.current.data = text
            if self.current._attrs:
                obj = self.current
            else:
                # a text only node is simply represented by the string
                obj = text or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(_name_mangle(name), obj)
        def characters(self, content):
            self.text_parts.append(content)

    builder = TreeBuilder()
    if isinstance(src,basestring):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    return builder.root._attrs.values()[0]

file = open(r"C:\Documents and Settings\pgarcia\My Documents\TESTENV\SYN\Payload.sxl", "r")

synoptyc = xml2obj(file.read())

asset = synoptyc.assets
fonts = asset.font

for font in fonts:
    print font.id
    
def getChoosers(start_id, units):
   
   choosers = ""
   for unit in units:
      chooser = """  <chooser defaultValue="*DEFAULT*" id="chooser{1}" annotation="{0} Color R">
   <pattern wildCard="false" regexp="0" value="200" minimal="false"/>
   <pattern wildCard="false" regexp="1" value="0" minimal="false"/>
  </chooser>
  <chooser defaultValue="*DEFAULT*" id="chooser{2}" annotation="{0} Color G">
   <pattern wildCard="false" regexp="0" value="0" minimal="false"/>
   <pattern wildCard="false" regexp="1" value="150" minimal="false"/>
  </chooser>
  <chooser defaultValue="*DEFAULT*" id="chooser{3}" annotation="{0} Color B">
   <pattern wildCard="false" regexp="25" minimal="false"/>
   <pattern wildCard="false" regexp="1" value="50" minimal="false"/>
  </chooser>"""
      chooser = chooser.format(unit, str(start_id), str(start_id+1), str(start_id+2))
      choosers += chooser + "\n"
      start_id += 3
   return choosers

def getBrush(name):
   global synoptyc
   asset = synoptyc.assets
   brushes = asset.brush
   for brush in brushes:
      if(brush.annotation==name):
         return brush.id
   
def getConnections(start_id, units):
   connections = ""
   
   for unit in units:
      connection = """  <connect dest="{0}" srcProp="output" destProp="r" src="chooser{1}"/>
  <connect dest="{0}" srcProp="output" destProp="g" src="chooser{2}"/>
  <connect dest="{0}" srcProp="output" destProp="b" src="chooser{3}"/>
  <connect dest="chooser{1}" srcProp="rawValue" destProp="input" src="param{1}"/>
  <connect dest="chooser{2}" srcProp="rawValue" destProp="input" src="param{1}"/>
  <connect dest="chooser{3}" srcProp="rawValue" destProp="input" src="param{1}"/>"""
      connection = connection.format(getBrush(unit), str(start_id), str(start_id+1), str(start_id+2))
      connections += connection + "\n"
      start_id += 3
   return connections
  
    

print(getChoosers(123, ["NSGU N Unit", "MISREC N Unit"]))

print(getConnections(123, ["NSGU N Unit", "MISREC N Unit"]))


    
    
    
    
    
