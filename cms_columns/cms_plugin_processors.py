from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string
import app_settings 

_current_row_width = 0

def columns(instance, placeholder, rendered_content, original_context):
    exclude_plugins = app_settings.get('CMS_COLUMNS_EXCLUDE_PLUGINS')
    if (instance.__class__.__name__ not in exclude_plugins) \
        and (not hasattr(settings, 'CMS_COLUMNS_PLACEHOLDERS') or placeholder.slot in settings.CMS_COLUMNS_PLACEHOLDERS):
            global _current_row_width
            if original_context['plugin']['first']:
                _current_row_width = 0

            column_width = None
            if hasattr(instance, 'column_width') and instance.column_width:
                column_width = int(instance.column_width)
                
            if column_width is not None or _current_row_width > 0:
            
                if column_width is None:
                    column_width = 100 - _current_row_width
            
                dict = {
                    'content': rendered_content,
                    'column_width': column_width,
                    #'plugin': original_context['plugin'],
                    'css_class': instance.__class__.__name__
                }
                if hasattr(instance, 'column_height'):
                    dict.update({'column_height': instance.column_height})
                    
                if hasattr(instance, 'first_column'):
                    first_column = instance.first_column
                else: 
                    first_column = _current_row_width == 0
                if first_column:
                    dict.update({'first_column': first_column})
                    
                _current_row_width += column_width

                if hasattr(instance, 'last_column'):
                    last_column = instance.last_column
                else: 
                    last_column = round(_current_row_width) >= 99
                if last_column:
                    dict.update({'last_column': last_column})
                    _current_row_width = 0
        
                if hasattr(instance, 'column_template'):
                    template = instance.column_template
                else:
                    template = app_settings.get('CMS_COLUMNS_TEMPLATE')
    
                template = template % {'framework': app_settings.get('CMS_COLUMNS_CSS_FRAMEWORK')}
                return render_to_string(template, Context(dict))

    return rendered_content