# Compare Beauty Products
## Business Objective
There are more than one million beauty products out there by different brands! What is the difference among the products within the same functional categories (e.g., creams, serum, and anti-aging) or even within the same brands? There are websites that provide you the ingredients in each product and give overall or individual ratings for the ingredients, but none of them tries to quantitatively compare the products based on their ingredients. **My motivation:** if we can quantify the relatedness among the products, we can answer questions such as what is the closest substitute to a specific product by this very expensive brand? **My goal:** to build an interactive website that can let users compare beauty products through interactive plots. Click [here](https://beauty-product.herokuapp.com) to access the website.

## Data Ingestion
The products' ingredient names were scraped from [skincarisma.com](https://www.skincarisma.com/) using Python requests and Beautiful Soup libraries. The code for scraping and process the data is in the data/scrap.ipynb notebook. The processed data are then stored in the data directory.

## Visualizations
I used altair to produce an interactive PCA plot where users can also color the dots by different types of labels. I also made various barplots in the images directory but these are not shown on the website.

## Machine Learning and Interactive Website
I used cosine similarity as the similarity score for the products and I used PCA plot to show how similar/different the products are. I built an interactive website where users can choose what products they want to compare. If the user chooses 1 product, he/she will get a table of products ranked by similarity score. If the user chooses 2 products, he/she will get a similarity score of the two products and a comparison table comparing the common and unique ingredients of the two products. If the user chooses 3 or more products, he/she will get a PCA plot on the products he/she chooses. If the user does not choose any products and hits the submit button, a PCA plot of all the products will be shown.

