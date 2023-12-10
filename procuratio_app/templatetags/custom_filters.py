from django import template

register = template.Library()

@register.filter(name='is_list')
def is_list(value):
    return isinstance(value, list)

@register.filter(name='is_dict')
def is_dict(value):
    return isinstance(value, dict)

@register.filter(name='group_by_attribute')
def group_by_attribute(products, attribute):
    grouped_products = {}
    for product in products:
        # Check if the product is a dictionary
        if isinstance(product, dict):
            attribute_value = product.get(attribute, '')
            # Remove the specified attribute from the product
            product.pop(attribute, None)
            if attribute_value in grouped_products:
                grouped_products[attribute_value].append(product)
            else:
                grouped_products[attribute_value] = [product]
    return grouped_products.items()