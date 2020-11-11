from flask import Flask, render_template, request
import pandas as pd
import json
import altair as alt
from sklearn.decomposition import PCA
from sklearn.feature_extraction import DictVectorizer
import dill
from sklearn.metrics import pairwise_distances

app = Flask(__name__)

@app.route('/')
def root():
    with open("data/data.json") as f:
        data = json.load(f)
    return render_template("index.html", data = data)

@app.route('/plot', methods=['POST'])
def plot():
    df_ingredient = pd.read_csv("data/ingredient_matrix.csv", index_col=0)
    merged_tb = pd.read_csv("data/merged_data_table.csv")
    product_ingredients = dill.load(open("data/product_ingre_dict.pkd", 'rb'))
    selected_products = request.form.getlist('products')
    pairwise_matrix = pd.DataFrame(pairwise_distances(df_ingredient.to_numpy(), metric="cosine"), columns=df_ingredient.index, index=df_ingredient.index)
    if not selected_products:
        ingredient_pca = PCA(n_components=2)
        PCs = ingredient_pca.fit_transform(df_ingredient)
        df_PCs = pd.DataFrame(PCs, columns=['PC1', 'PC2'])
        df_PCs['Name'] = df_ingredient.index
        df_PCs['Brand'] = merged_tb['Brand']
        df_PCs['Function'] = merged_tb['Function']
        df_PCs['Category'] = merged_tb['Category']
        input_dropdown = alt.binding_select(options=['Brand','Function','Category'])
        selection = alt.selection_single(name='Color By', fields=['column'], bind=input_dropdown, init={'column':'Function'})
        chart = alt.Chart(df_PCs).transform_fold(['Brand', 'Function', 'Category'], as_=['column', 'value']).transform_filter(selection).mark_point().encode(x="PC1:Q", y="PC2:Q", color="value:N", column="column:N", tooltip=['Name:N']).add_selection(selection)
        return render_template("plot.html", chart=chart.to_json())
    elif len(selected_products) >= 3:    
        print("recalculate PC")
        ingredient_ls = []
        product_name = []
        for k, v in product_ingredients.items():
            if k in selected_products:
                product_name.append(k)
                ingredient_dict = {}
                for each_ingre in v:
                    ingredient_dict[each_ingre] = 1
                ingredient_ls.append(ingredient_dict)
        transform_ingre = DictVectorizer()
        ingredient_matrix = transform_ingre.fit_transform(ingredient_ls).toarray()
        col_names = transform_ingre.get_feature_names()
        df_ingredient = pd.DataFrame(ingredient_matrix, columns=col_names, index = product_name)
        ingredient_pca = PCA(n_components=2)
        PCs = ingredient_pca.fit_transform(df_ingredient)
        df_PCs = pd.DataFrame(PCs, columns=['PC1', 'PC2'])
        df_PCs['Name'] = df_ingredient.index
        brand =  []
        function = []
        category = []
        for name in df_ingredient.index:
            #print(name)
            row = merged_tb[merged_tb['Name']==name]
            brand.extend(row['Brand'].tolist())
            function.extend(row['Function'].tolist())
            category.extend(row['Category'].tolist())
        #print(brand)
        #print(function)
        #print(category)
        df_PCs['Brand'] = brand
        df_PCs['Function'] = function
        df_PCs['Category'] = category
        input_dropdown = alt.binding_select(options=['Brand','Function','Category'])
        selection = alt.selection_single(name='Color By', fields=['column'], bind=input_dropdown, init={'column':'Function'})
        chart = alt.Chart(df_PCs).transform_fold(['Brand', 'Function', 'Category'], as_=['column', 'value']).transform_filter(selection).mark_point().encode(x="PC1:Q", y="PC2:Q", color="value:N", column="column:N", tooltip=['Name:N']).add_selection(selection)
        return render_template("plot.html", chart=chart.to_json())
        
        '''
        print("not recalculate")
        df_ingredient.reset_index(inplace=True)
        new_df = df_ingredient.query(f'index in {selected_products}')
        new_df.set_index('index', inplace=True)
        ingredient_pca = PCA(n_components=2)
        PCs = ingredient_pca.fit_transform(new_df)
        df_PCs = pd.DataFrame(PCs, columns=['PC1', 'PC2'])
        df_PCs['Name'] = new_df.index
        brand =  []
        function = []
        category = []
        for name in new_df.index:
            #print(name)
            row = merged_tb[merged_tb['Name']==name]
            brand.extend(row['Brand'].tolist())
            function.extend(row['Function'].tolist())
            category.extend(row['Category'].tolist())
        #print(brand)
        #print(function)
        #print(category)
        df_PCs['Brand'] = brand
        df_PCs['Function'] = function
        df_PCs['Category'] = category
        input_dropdown = alt.binding_select(options=['Brand','Function','Category'])
        selection = alt.selection_single(name='Color By', fields=['column'], bind=input_dropdown, init={'column':'Function'})
        chart = alt.Chart(df_PCs).transform_fold(['Brand', 'Function', 'Category'], as_=['column', 'value']).transform_filter(selection).mark_point().encode(x="PC1:Q", y="PC2:Q", color="value:N", column="column:N", tooltip=['Name:N']).add_selection(selection)
        return render_template("plot.html", chart=chart.to_json())
        '''
    
    elif len(selected_products) == 1:
        #print(df_ingredient.head())       
        col = pairwise_matrix[selected_products[0]]
        sorted_col = col.sort_values()
        output = [[k, v] for k, v in sorted_col.items()]
        print(output)
        return render_template("plot1.html", data = output)

    elif len(selected_products) == 2:
        col = pairwise_matrix[selected_products[0]]
        row = col[col.index==selected_products[1]]
        val = row.values[0]
        mgrow1 = merged_tb[merged_tb['Name']==selected_products[0]]['0'].values[0]
        mgrow2 = merged_tb[merged_tb['Name']==selected_products[1]]['0'].values[0]
        #print(mgrow1)
        ingre1 = [x.strip("'") for x in mgrow1.strip("][").split(", ")]
        ingre2 = [x.strip("'") for x in mgrow2.strip("][").split(", ")]
        common = list(set(ingre1).intersection(ingre2))
        common = ", ".join(common)
        ingre1_unique = list(set(ingre1) - set(ingre2))
        ingre1_unique = ", ".join(ingre1_unique)
        ingre2_unique = list(set(ingre2) - set(ingre1))
        ingre2_unique = ", ".join(ingre2_unique)
        product1 = selected_products[0]
        product2 = selected_products[1]
        return render_template("plot2.html", product1=product1, product2=product2, val=val, common=common, ingre1=ingre1_unique, ingre2=ingre2_unique)




if __name__ == '__main__':
    app.run(debug=True)