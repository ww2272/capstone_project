from flask import Flask, render_template, request
import pandas as pd
import json
import altair as alt
from sklearn.decomposition import PCA

app = Flask(__name__)

with open("../data/data.json") as f:
    data = json.load(f)

df_ingredient = pd.read_csv("../data/ingredient_matrix.csv", index_col=0)
#df_ingredient.head()

merged_tb = pd.read_csv("../data/merged_data_table.csv")
print(merged_tb.head())


@app.route('/')
def root():
    return render_template("index.html", data = data)

@app.route('/plot', methods=['POST'])
def plot():
    selected_products = request.form.getlist('products')
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
        alt.Chart(df_PCs).transform_fold(['Brand', 'Function', 'Category'], as_=['column', 'value']).transform_filter(selection).mark_point().encode(x="PC1:Q", y="PC2:Q", color="value:N", column="column:N", tooltip=['Name:N']).add_selection(selection)
        return render_template("plot.html", chart=chart.to_json())
    else:
        pass




if __name__ == '__main__':
    app.run(debug=True)