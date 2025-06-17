/*
The 'color' table contains the following columns:

'id' stores the unique ID for each color.
'name' stores the name of the color.
'extra_fee' stores the extra charge (if any) added for clothing ordered in this color.

In the 'customer' table, you'll find the following columns:

'id' stores customer IDs.
'first_name' stores the customer's first name.
'last_name' stores the customer's last name.
'favorite_color_idstores' the ID of the customer's favorite color (references the color table).

The 'category' table contains these columns:

'id' stores the unique ID for each category.
'name' stores the name of the category.
'parent_id' stores the ID of the main category for this category (if it's a subcategory). 
If this value is NULL, it denotes that this category is a main category. 
Note: Values are related to those in the id column in this table.

The 'clothing' table stores data in the following columns:

'id' stores the unique ID for each item.
'name' stores the name of that item.
'size' stores the size of that clothing: S, M, L, XL, 2XL, or 3XL.
'price' stores the item's price.
'color_id' stores the item's color (references the color table).
'category_id' stores the item's category (references the category table).

The 'clothing_order' table contains the following columns:

'id' stores the unique order ID.
'customer_id' stores the ID of the customer ordering the clothes (references the customer table).
'clothing_id' stores the ID of the item ordered (references the clothing table).
'items' stores how many of that clothing item the customer ordered.
'order_date' stores the date of the order.

Task 1:
Display the name of clothing items (name the column clothes), their color (name the column color), and the last name and first
name of the customer(s) who bought this apparel in their favorite color. Sort rows according to color, in ascending order.

Task 2:
Select the last name and first name of customers and the name of their favorite color for customers with no purchases.
*/

-- Task_1

SELECT  cl.name as clothes, 
        col.name as color,
        cus.first_name,
        cus.last_name
FROM clothing_order as ord
JOIN clothing cl ON ord.clothing_id = cl.id
JOIN color col ON col.id = cl.color_id
JOIN customers cus ON cus.id = ord. customer_id
WHERE cus.favorite_color_id = cl.color_id
ORDER BY col.name

-- Task_2
SELECT  cus.first_name,
        cus.last_name,
        col.name as color
FROM customer cus
WHERE cus.id NOT IN (SELECT DISTINCT(customer_id) FROM clothing_order)
JOIN color col ON cus.favorite_color_id = col.id



