import pandas as pd
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
nltk.download('wordnet')
import sys
def get_data(s):
    x=pd.read_csv(s)
    x=x[["ingredients", "name"]]
    return(x.values.tolist())
def pre1(ing_name):
    for i in ing_name:
        if(type(i[0])!=float):
            s=i[0].split(',')
            l=[]
            for j in s:
                x=j.split(' ')
                l.extend(x)
            i[0]=l
        else:
            i[0]=['none']
    return(ing_name)


def pre2(ing_name):
    key = ['olive','4\u2009½', '¼', '3\u2009½', 'and', 'peeled', 'finely', 'frozen', 'can', 'as', 'needed', 'cubed', 'large',
           'small', 'cooked', 'all-purpose', 'optional', 'minced', '¾', 'fresh', 'or', '(Optional)', 'more', 'to',
           'quartered', 'sliced', 'tablespoon', 'ground', 'teaspoons', 'teaspoon', ' ', '', '½', 'tablespoons',
           'grated', 'cup', 'diced', 'cups', 'chopped', 'chop', '1\u2009½']
    all_ing=[]
    all_ing1=["salt",'jalapeno','choy','bay','whole-milk','soda','chitterlings','chicken','chili','ice','coconutmilk','anise','cocoa','oat','chia','maple','pepper','beef',"water","oil","butter", "eggs", "milk", "parmesan", "cheddar", "american cheese", "sour cream","masa","cream cheese","tapioca","cake-mix","mozzarella", "yogurt", "cream", "evaporated milk", "whipped cream", "half and half", "feta", "monterey jack cheese", "condensed milk", "cottage cheese", "ice cream", "swiss cheese", "velveeta", "frosting", "buttermilk", "ricotta", "goat cheese", "provolone", "blue cheese", "powdered milk", "colby cheese", "pepper jack", "italian cheese", "soft cheese", "gouda", "pepperjack cheese", "romano", "brie", "pizza cheese", "ghee", "creme fraiche", "cheese soup", "gruyere", "pecorino cheese", "custard", "muenster", "queso fresco cheese", "hard cheese", "havarti cheese", "asiago", "mascarpone", "neufchatel", "halloumi", "paneer", "brick cheese", "camembert cheese", "goat milk", "garlic herb cheese", "edam cheese", "manchego", "fontina", "stilton cheese", "emmenthaler cheese", "red leicester cheese", "jarlsberg cheese", "bocconcini cheese", "farmer cheese",'oyster', 'veal', 'clam', 'pork', 'beef', ' lamb', 'chicken', 'turkey', 'duck', 'rabbit', ' seafood','goat', 'egg', 'shrimp','sauce','soy','brussel','sprout','cheese','prawn', 'crab', 'salmon', 'tuna', 'mutton', 'sausage', 'peper', 'pepperoni','Ham', 'caviar', 'camel', 'octopus', 'squid', 'meat', 'fish', 'cod', 'herring', 'rabbit', 'quail','ribs', "creme de cassis", "wensleydale cheese", "longhorn cheese", "double gloucester cheese", "raclette cheese", "lancashire cheese", "cheshire cheese", "onion", "garlic", "tomato", "potato", "carrot", "bell pepper", "basil", "parsley", "broccoli", "corn", "spinach", "mushroom", "green beans", "ginger", "chili pepper", "celery", "rosemary", "salad greens", "red onion", "cucumber", "sweet potato", "pickle", "avocado", "zucchini", "cilantro", "frozen vegetables", "olive", "asparagus", "cabbage", "cauliflower", "dill", "kale", "mixed vegetable", "pumpkin", "squash", "mint", "scallion", "sun dried tomato", "shallot", "eggplant", "beet", "butternut squash", "horseradish", "leek", "caper", "brussels sprout", "artichoke heart", "chia seeds", "radish", "sauerkraut", "artichoke", "portobello mushroom", "sweet pepper", "arugula", "spaghetti squash", "capsicum", "bok choy", "parsnip", "okra", "yam", "fennel", "turnip", "snow peas", "bean sprouts", "seaweed", "chard", "collard", "canned tomato", "pimiento", "watercress", "tomatillo", "rocket", "mustard greens", "bamboo shoot", "rutabaga", "endive", "broccoli rabe", "jicama", "kohlrabi", "hearts of palm", "butternut", "celery root", "daikon", "radicchio", "porcini", "chinese broccoli", "jerusalem artichoke", "cress", "water chestnut", "dulse","gourd","beans","curry","micro greens", "burdock", "chayote", "sweet corn","lemon", "apple", "banana", "lime", "strawberries", "orange", "pineapple", "blueberries", "raisin", "coconut", "grape", "peach", "raspberries", "cranberries", "mango", "pear", "blackberries", "cherry", "date", "watermelon", "berries", "kiwi", "grapefruit", "mandarin", "craisins", "cantaloupe", "plum", "apricot", "clementine", "prunes", "apple butter", "pomegranate", "nectarine", "fig", "tangerine", "papaya", "rhubarb", "sultanas", "plantain", "currant", "passion fruit", "guava", "persimmons", "lychee", "lingonberry", "tangelos", "kumquat", "boysenberry", "star fruit", "quince", "honeydew", "crabapples","rice", "pasta", "flour", "bread", "baking powder", "baking soda", "bread crumbs", "cornstarch", "rolled oats", "noodle", "flour tortillas", "pancake mix", "yeast", "cracker", "quinoa", "brown rice", "cornmeal", "self rising flour", "cake mix", "saltines", "popcorn", "macaroni cheese mix", "corn tortillas", "ramen", "cereal", "biscuits", "stuffing mix", "couscous", "pie crust", "bisquick", "chips", "angel hair", "coconut flake", "bread flour", "croutons", "lasagne", "pizza dough", "bagel", "puff pastry", "hot dog bun", "barley", "multigrain bread", "potato flakes", "pretzel", "cornbread", "english muffin", "cornflour", "crescent roll dough", "cream of wheat", "coconut flour", "pita", "risotto", "muffin mix", "bicarbonate of soda", "ravioli", "wheat", "rice flour", "polenta", "baguette", "gnocchi", "vermicelli", "semolina", "wheat germ", "buckwheat", "croissants", "bread dough", "filo dough", "yeast flake", "pierogi", "matzo meal", "rye", "tapioca flour", "shortcrust pastry", "potato starch", "breadsticks", "ciabatta", "spelt", "angel food", "tapioca starch", "starch", "whole wheat flour", "gram flour", "sourdough starter", "wafer", "bran", "challah", "sponge cake", "malt extract", "sorghum flour","sugar", "brown sugar", "honey", "confectioners sugar", "maple syrup", "syrup", "corn syrup", "molasses", "artificial sweetener", "agave nectar","cinnamon", "vanilla", "garlic powder", "paprika", "oregano", "chili powder", "red pepper flake", "cumin", "cayenne", "italian seasoning", "thyme", "onion powder", "nutmeg", "ground nutmeg", "curry powder", "bay leaf", "taco seasoning", "sage", "clove", "allspice", "turmeric", "chive", "peppercorn", "ground coriander", "cajun seasoning", "coriander", "celery salt", "vanilla essence", "herbs", "steak seasoning", "poultry seasoning", "chile powder", "cardamom", "italian herbs", "tarragon", "garam masala", "marjoram", "mustard seed", "celery seed", "chinese five spice", "italian spice", "saffron", "onion flake", "herbes de provence", "chipotle", "dill seed", "fennel seed", "caraway", "cacao", "star anise", "savory", "chili paste", "tamarind", "aniseed", "fenugreek", "lavender", "old bay seasoning", "lemon balm","chicken breast", "ground beef", "bacon", "sausage", "beef steak", "ham", "hot dog", "pork chops", "chicken thighs", "ground turkey", "cooked chicken", "turkey", "pork", "pepperoni", "whole chicken", "chicken leg", "ground pork", "chorizo", "chicken wings", "beef roast", "polish sausage", "salami", "pork roast", "ground chicken", "pork ribs", "spam", "venison", "pork shoulder", "bologna", "bratwurst", "prosciutto", "lamb", "corned beef", "chicken roast", "lamb chops", "pancetta", "ground lamb", "beef ribs", "duck", "pork belly", "beef liver", "leg of lamb", "canadian bacon", "beef shank", "veal", "chicken giblets", "cornish hen", "lamb shoulder", "lamb shank", "deer", "ground veal", "pastrami", "rabbit", "sliced turkey", "pork loin", "elk", "beef suet", "veal cutlet", "lamb loin", "marrow bones", "goose", "chicken tenders", "veal chops", "quail", "oxtail", "pheasant", "lamb liver", "moose", "turkey liver", "pork liver", "veal shank", "foie gras", "beef sirloin", "liver sausage","pig","roast","sweetbread", "wild boar", "snail", "pigeon", "duck liver", "goose liver", "grouse", "ostrich", "soppressata", "alligator","canned tuna", "salmon","fish","tilapia", "fish fillets", "cod", "canned salmon", "anchovies", "smoked salmon", "sardines", "tuna steak", "whitefish", "halibut", "trout", "haddock", "flounder", "catfish", "mahi mahi", "mackerel", "sole", "sea bass", "red snapper", "swordfish", "pollock", "herring", "perch", "grouper", "caviar", "monkfish", "rockfish", "lemon sole", "pike", "barramundi", "eel", "bluefish", "carp", "cuttlefish", "pompano", "arctic char", "john dory", "marlin", "amberjack", "sturgeon","shrimp", "crab", "prawns", "scallop", "clam", "lobster", "mussel", "oyster", "squid", "calamari", "crawfish", "octopus", "cockle", "conch", "sea urchin","mayonnaise", "ketchup", "mustard", "vinegar", "soy sauce", "balsamic vinegar", "worcestershire", "hot sauce", "barbecue sauce", "ranch dressing", "wine vinegar", "apple cider vinegar", "cider vinegar", "italian dressing", "rice vinegar", "salad dressing", "tabasco", "fish sauce", "teriyaki", "steak sauce", "tahini", "enchilada sauce", "vinaigrette dressing", "oyster sauce", "honey mustard", "sriracha", "caesar dressing", "taco sauce", "mirin", "blue cheese dressing", "sweet and sour sauce", "thousand island", "picante sauce", "buffalo sauce", "french dressing", "tartar sauce", "cocktail sauce", "marsala", "adobo sauce", "tzatziki sauce", "sesame dressing", "ponzu", "duck sauce", "pickapeppa sauce", "yuzu juice", "cream sauce","olive oil", "vegetable oil", "cooking spray", "canola oil", "shortening", "sesame oil", "coconut oil", "peanut oil", "sunflower oil", "lard", "grape seed oil", "corn oil", "almond oil", "avocado oil", "safflower oil", "walnut oil", "hazelnut oil", "palm oil", "soybean oil", "mustard oil", "pistachio oil","soya oil","bouillon", "ground ginger", "sesame seed", "cream of tartar", "chili sauce", "soya sauce", "apple cider", "hoisin sauce", "liquid smoke", "rice wine", "vegetable bouillon", "poppy seed", "balsamic glaze", "miso", "wasabi", "fish stock", "rose water", "pickling salt", "champagne vinegar", "bbq rub", "jamaican jerk spice", "accent seasoning", "pickling spice", "mustard powder", "mango powder", "adobo seasoning", "kasuri methi", "caribbean jerk seasoning", "brine", "matcha powder", "cassia","tomato sauce", "tomato paste", "salsa", "pesto", "alfredo sauce", "beef gravy", "curry paste", "chicken gravy", "cranberry sauce", "turkey gravy", "mushroom gravy", "sausage gravy", "onion gravy", "cream gravy", "pork gravy", "tomato gravy","giblet gravy","green beans", "peas", "black beans", "chickpea", "lentil", "refried beans", "hummus", "chili beans", "lima beans", "kidney beans", "pinto beans", "edamame", "split peas", "snap peas", "soybeans", "cannellini beans", "navy beans", "french beans", "red beans", "great northern beans","fava beans","white wine", "beer", "red wine", "vodka", "rum", "whiskey", "tequila", "sherry", "bourbon", "cooking wine", "whisky", "liqueur", "brandy", "gin", "kahlua", "irish cream", "triple sec", "champagne", "amaretto", "cabernet sauvignon", "vermouth", "bitters", "maraschino", "sake", "grand marnier", "masala", "dessert wine", "schnapps", "port wine", "sparkling wine", "cognac", "chocolate liqueur", "burgundy wine", "limoncello", "creme de menthe", "bloody mary", "raspberry liquor", "curacao", "frangelico", "shaoxing wine", "absinthe", "madeira wine", "ouzo", "anisette", "grappa", "ciclon", "drambuie","peanut butter", "almond", "walnut", "pecan", "peanut", "cashew", "flax", "pine nut", "pistachio", "almond meal", "hazelnut", "macadamia", "almond paste", "chestnut", "praline", "macaroon","margarine", "coconut milk", "almond milk", "soy milk", "rice milk", "hemp milk", "non dairy creamer","chocolate", "apple sauce", "strawberry jam", "graham cracker", "marshmallow", "chocolate syrup", "potato chips", "nutella", "chocolate morsels", "bittersweet chocolate", "pudding mix", "raspberry jam", "dark chocolate", "chocolate chips", "jam", "white chocolate", "brownie mix", "chocolate pudding", "jello", "caramel", "chocolate powder", "candy", "corn chips", "cookies", "apricot jam", "chocolate bar", "cookie dough", "oreo", "doritos", "chocolate cookies", "butterscotch", "blackberry preserves", "blueberry jam", "peach preserves", "cherry jam", "fig jam", "plum jam", "cinnamon roll", "fudge", "cookie crumb", "grape jelly", "chilli jam", "lady fingers", "pound cake", "black pudding", "chocolate wafer", "gummy worms", "biscotti biscuit", "doughnut", "amaretti cookies", "apple jelly", "red pepper jelly", "orange jelly", "jalapeno jelly", "mint jelly", "currant jelly", "lemon jelly", "quince jelly","coffee", "orange juice", "tea", "green tea", "apple juice", "tomato juice", "coke", "chocolate milk", "pineapple juice", "lemonade", "cranberry juice", "espresso", "fruit juice", "ginger ale", "club soda", "sprite", "kool aid", "grenadine", "margarita mix", "cherry juice", "pepsi", "mountain dew"]
    for i in all_ing1:
        all_ing.append(lemmatizer.lemmatize(i.lower()))
    for i in ing_name:
        a = []
        b=[]
        if (type(i[0]) != float):
            for j in i[0]:
                if (j.isdigit() == False and j not in key):
                    if(lemmatizer.lemmatize(j.lower()) in all_ing):
                        a.append(lemmatizer.lemmatize(j.lower()))
                    else:
                        b.append(lemmatizer.lemmatize(j.lower()))
            i[0] = a
            print(i[0])
            print(b)
            print('\n')
        else:
            i[0] = ['none']
    return (ing_name)
def add_keywords_to_csv(dataset,ing):
    data = pd.read_csv(dataset)
    keys=[]
    for i in ing:
        keys.append(i[0])
    data['keyword'] = keys
    data.to_csv(dataset,index=False)
    data.drop(data.filter(regex="Unnamed"),axis=1, inplace=True)
    return(data)
def add_nonveg_to_csv(dataset,ing,non_veg):
    nv = pd.read_csv(dataset)
    keys=[]
    for i in ing:
        isnv=0
        for j in i[0]:
            if(lemmatizer.lemmatize(j.lower()) in non_veg):
                isnv=1
                break
        if(isnv==1):
            keys.append('non-veg')
        else:
            keys.append('veg')
    nv['veg/nonveg'] = keys
    nv.to_csv(dataset,index=False)
    nv.drop(data.filter(regex="Unnamed"),axis=1, inplace=True)
    return(nv)
if __name__ == '__main__':
    ing_name_indian=get_data("recipes_dataset/indian.csv")
    ing_name_dessert=get_data("recipes_dataset/dessert.csv")
    ing_name_diabetic=get_data("recipes_dataset/diabetic.csv")
    ing_name_side_dish=get_data("recipes_dataset/side_dish.csv")
    ing_name_salad=get_data("recipes_dataset/salad.csv")
    ing_name_gluten_free=get_data("recipes_dataset/gluten_free.csv")
    ing_name_keto=get_data("recipes_dataset/keto.csv")
    ing_name_low_carb=get_data("recipes_dataset/low_carb.csv")
    ing_name_mocktail=get_data("recipes_dataset/mocktail.csv")
    ing_name_smoothie=get_data("recipes_dataset/smoothie.csv")

    ing_name_indian = pre1(ing_name_indian)
    ing_name_indian = pre2(ing_name_indian)
    ing_name_dessert = pre1(ing_name_dessert)
    ing_name_dessert = pre2(ing_name_dessert)
    ing_name_diabetic = pre1(ing_name_diabetic)
    ing_name_diabetic = pre2(ing_name_diabetic)
    ing_name_side_dish = pre1(ing_name_side_dish)
    ing_name_side_dish = pre2(ing_name_side_dish)
    ing_name_salad = pre1(ing_name_salad)
    ing_name_salad = pre2(ing_name_salad)
    ing_name_gluten_free = pre1(ing_name_gluten_free)
    ing_name_gluten_free = pre2(ing_name_gluten_free)
    ing_name_keto = pre1(ing_name_keto)
    ing_name_keto = pre2(ing_name_keto)
    ing_name_low_carb = pre1(ing_name_low_carb)
    ing_name_low_carb = pre2(ing_name_low_carb)
    ing_name_mocktail = pre1(ing_name_mocktail)
    ing_name_mocktail = pre2(ing_name_mocktail)
    ing_name_smoothie = pre1(ing_name_smoothie)
    ing_name_smoothie = pre2(ing_name_smoothie)
    datasets = ['recipes_dataset/indian.csv', 'recipes_dataset/dessert.csv', 'recipes_dataset/diabetic.csv',
                'recipes_dataset/side_dish.csv', 'recipes_dataset/salad.csv', 'recipes_dataset/gluten_free.csv',
                'recipes_dataset/keto.csv', 'recipes_dataset/low_carb.csv', 'recipes_dataset/mocktail.csv',
                'recipes_dataset/smoothie.csv']
    ings = [ing_name_indian, ing_name_dessert, ing_name_diabetic, ing_name_side_dish, ing_name_salad,
            ing_name_gluten_free, ing_name_keto, ing_name_low_carb, ing_name_mocktail, ing_name_smoothie]
    for i in range(0, len(datasets)):
        data = add_keywords_to_csv(datasets[i], ings[i])
    non_veg = ['oyster', 'veal', 'clam','pig','steak','roast','pork', 'beef', ' lamb', 'chicken', 'turkey', 'duck', 'rabbit', ' seafood',
               'goat', 'egg', 'shrimp', 'prawn', 'crab', 'salmon', 'tuna', 'mutton', 'sausage', 'peper', 'pepperoni',
               'Ham', 'caviar', 'camel', 'octopus', 'squid', 'meat', 'fish', 'cod', 'herring', 'rabbit', 'quail','ribs']
    for i in range(0, len(datasets)):
        non = add_nonveg_to_csv(datasets[i], ings[i], non_veg)
        non.head()