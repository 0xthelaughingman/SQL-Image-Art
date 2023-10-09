# SQL Image Art

A Python(3.8) demonstration of image manipulation to get an output that can be rendered as an SQL(Snowflake) bar chart.

## Theory

The method relies on finding the maximum number of segments in the image's pixel columns.
Once the maximum segments has been obtained, it's just a matter of computing the exact lengths of the said segments for the entirety of the image.
The result is a set of arrays that can be easy manipulated in either SQL flavours and presented as a ***stacked*** bar chart.

Example: (5 Segments highlighted for the column)

![5 Segments highlighted for the column](./theory.png?raw=true "Segments Example")


## Dependencies

- Python 3.8
- opencv