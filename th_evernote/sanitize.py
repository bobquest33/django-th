# coding: utf-8
import re

# sanitize use from
# https://raw.github.com/mindprince/pinboardToEvernote/master/sanitize.py
# and modifiy with the adding of the 2nd line
from tidylib import *
from xml.dom.minidom import *


def sanitize(html):
    # with from __future__ import unicode_litterals
    # tidy_document does not want other options at all
    # such as div merge char-encoding and so on
    document, errors = tidy_document(
        html, options={"output-xhtml": 1, "force-output": 1})

    parsed_dom = xml.dom.minidom.parseString(document)
    document_element = parsed_dom.documentElement
    remove_prohibited_elements(document_element)
    remove_prohibited_attributes(document_element)
    body = document_element.getElementsByTagName("body")[0]
    body.tagName = "en-note"
    return body.toxml()


def remove_prohibited_elements(document_element):
    """
        To fit the Evernote DTD need, drop this tag name
    """
    prohibited_tag_names = [
        "applet", "base", "basefont", "bgsound", "blink", "button", "dir",
        "embed", "fieldset", "form", "frame", "frameset", "head", "iframe",
        "ilayer", "input", "isindex", "label", "layer", "legend", "link",
        "marquee", "menu", "meta", "noframes", "noscript", "object",
        "optgroup", "option", "param", "plaintext", "script", "select",
        "style", "textarea", "xml", ]
    for tag_name in prohibited_tag_names:
        remove_prohibited_element(tag_name, document_element)


def remove_prohibited_element(tag_name, document_element):
    """
        To fit the Evernote DTD need, drop this tag name
    """
    elements = document_element.getElementsByTagName(tag_name)
    for element in elements:
        p = element.parentNode
        p.removeChild(element)


def remove_prohibited_attributes(element):
    """
        To fit the Evernote DTD need, drop this attribute name
    """
    prohibited_attributes = ["id", "class", "onclick", "ondblclick", "onload",
                             "accesskey", "data", "dynsrc", "tabindex",
                             "onmouseover", "onmouseout", "onblur",
                             "frame", "rules", "width",  "data-shortcode"]
    # FIXME All on* attributes are prohibited. How to use a regular expression
    # as argument to remove_attribute?
    for attribute in prohibited_attributes:
        try:
            element.removeAttribute(attribute)
        except xml.dom.NotFoundErr:
            pass
    try:
        if element.hasAttribute("href"):
            t = element.toxml()
            if re.search('href="http', t) or re.search('href="https', t):
                pass
            else:
                element.removeAttribute("href")
    except:
        pass

    list_on_children = element.childNodes
    for child in list_on_children:
        if child.nodeType == 1:
            remove_prohibited_attributes(child)
