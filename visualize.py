import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import wordcloud
import itertools

DATES = ['03-01-2023T21:45:43Z', '20-12-2022T23:31:37Z']
CATEGORIES = {1: 'Film & Animation',
              2: 'Autos & Vehicles',
              10: 'Music',
              15: 'Pets & Animals',
              17: 'Sports',
              18: 'Short Movies',
              19: 'Travel & Events',
              20: 'Gaming',
              21: 'Videoblogging',
              22: 'People & Blogs',
              23: 'Comedy',
              24: 'Entertainment',
              25: 'News & Politics',
              26: 'Howto & Style',
              27: 'Education',
              28: 'Science & Technology',
              29: 'Nonprofits & Activism',
              30: 'Movies',
              31: 'Anime/Animation',
              32: 'Action/Adventure',
              33: 'Classics',
              34: 'Comedy',
              35: 'Documentary',
              36: 'Drama',
              37: 'Family',
              38: 'Foreign',
              39: 'Horror',
              40: 'Sci-Fi/Fantasy',
              41: 'Thriller',
              42: 'Shorts',
              43: 'Shows',
              44: 'Trailers'}


def plot_1(dataframe):
    '''
    Author: Minh
    '''
    def func(pct, allvalues):
        absolute = int(pct / 100.*np.sum(allvalues))
        return "{:.1f}%\n({:d}pts)".format(pct, absolute)

    # create 2 arrays to hold the categories' names and its popularity point
    categories = []
    for i in CATEGORIES.keys():
        categories.append(CATEGORIES[i])
    popularity = [0]*len(categories)

    # populate arrays with popularity point
    for i in dataframe.index:
        t = categories.index(CATEGORIES[dataframe.loc[i, 'category_id']])
        popularity[t] += dataframe.loc[i, 'notes']

    # create dataset and sort by total popularity
    dataset = pd.DataFrame(
        data={'categories': categories, 'popularity': popularity})
    dataset = dataset.groupby('categories').sum().sort_values(
        by=['popularity'], ascending=False)

    # take top 5 categories
    dataset_top = dataset[:5].copy()

    # one entry for all other categories
    dataset_others = pd.DataFrame(
        data={'popularity': [dataset['popularity'][5:].sum()]}, index=['Others'])

    # combining top 5 with others
    dataset = pd.concat([dataset_top, dataset_others])

    # plot pie chart
    colors = ['#00c2f9', '#00e4b9', '#feeaae', '#fcb1d9', '#fdfdfa', '#d9ccb2']
    plt.pie(dataset['popularity'], labels=dataset.index,
            shadow=False, colors=colors,
            autopct=lambda pct: func(pct, dataset['popularity']))
    plt.show()


def plot_2(dataframe):
    '''
    Author: Huy
    Consider the top 5 most frequently trending categories.
    How many views in average does it take for a video of a certain category to trend?	
    '''
    # fill frequency table of categories
    frequency = {}
    for _, row in dataframe.iterrows():
        try:
            frequency[CATEGORIES[row['category_id']]]['videos'] += 1
            frequency[CATEGORIES[row['category_id']]
                      ]['views'] += row['view_count']
        except:
            frequency[CATEGORIES[row['category_id']]] = {
                'videos': 1, 'views': row['view_count']}
    sorted_frequency = dict(
        sorted(frequency.items(), key=lambda k_v: k_v[1]['videos'], reverse=True))

    top_categories = dict(itertools.islice(sorted_frequency.items(), 8))

    # calculate average view counts
    average = []
    for category in top_categories.values():
        average.append(category['views'] // category['videos'])

    dataset = pd.DataFrame(data={
        'categories': [*top_categories.keys()],
        'average_view_count': average,
    })

    # plot data
    _, ax = plt.subplots()
    ax.bar(dataset['categories'], dataset['average_view_count'])
    ax.set_xlabel('Most frequently trending categories (left to right)')
    ax.set_ylabel('Average number of videos per category')
    ax.set_title(
        'How many views in average does it take for a video of a certain category to trend?')
    for i, v in enumerate(dataset['average_view_count']):
        ax.text(i - 0.15, v + 15000, " " + str(v))
    # show plot
    plt.show()


def plot_4(dataframe):
    '''
    Author: ...
    Does a special event affect the YouTube trending tab?
    '''
    keywords = ['christmas', 'xmas', 'holiday', 'santa', 'snow', 'noel', 'present', 'gift', 'new year',
                '???????????????', '????????????', '?????????', '?????????', '???', '?????????', '??????',
                'kurisumasu', 'horid??', 'horidee', 'yuki', 'noeru', 'okurimono', "shin'nen",
                '???????????????', '??????', '??????', '???', '??????', '??????', '??????',
                'keuliseumaseu', 'hyuil', 'nun', 'hyeonjae', 'seonmul', 'saehae',
                '?????????????????????', '?????????????????? ?????? ?????????', '???????????????', '????????????', '????????????', '?????????????????????', '???????????????', '????????? ?????????'
                'krisamas', 'chhuttee ka din', 'saanta', 'barph', 'vartamaan', 'upahaar', 'naya saal']

    df_before_holiday = dataframe[dataframe['trending_date'] == DATES[0]]
    df_during_holiday = dataframe[dataframe['trending_date'] == DATES[1]]

    # count holiday-related videos
    # before holiday
    count_before = 0
    for _, row in df_before_holiday.iterrows():
        if any(keyword in row['title'].lower() for keyword in keywords) or any(keyword in row['description'].lower() for keyword in keywords):
            count_before += 1
    # during holiday
    count_during = 0
    for _, row in df_during_holiday.iterrows():
        if any(keyword in row['title'].lower() for keyword in keywords) or any(keyword in row['description'].lower() for keyword in keywords):
            count_during += 1

    # prepare data for plot
    total = [len(df_before_holiday), len(df_during_holiday)]
    related = [count_before, count_during]
    non_related = [total[0] - related[0], total[1] - related[1]]
    labels = ['before holiday (total = {0} videos)'.format(total[0]),
              'after holiday (total = {0} videos)'.format(total[1])]

    # plot data
    _, ax = plt.subplots()
    # create stacked bars
    ax.bar(labels, non_related, label='non-related')
    ax.bar(labels, related, bottom=non_related, label='related')
    # show percentage of non-relted videos
    for i in range(len(ax.patches)):
        rec = ax.patches[i]
        if i < 2:
            ax.text(ax.patches[i].get_x() + ax.patches[i].get_width() / 2, ax.patches[i].get_y() + ax.patches[i].get_height() / 2,
                    "{pct:.1f}%\n({num} videos)".format(
                        pct=(non_related[i] / total[i]) * 100, num=non_related[i]),
                    ha='center', va='bottom')
        else:
            ax.text(ax.patches[i].get_x() + ax.patches[i].get_width() / 2, ax.patches[i].get_y() + ax.patches[i].get_height() / 2,
                    "{pct:.1f}%\n({num} videos)".format(
                        pct=(related[i - 2] / total[i - 2]) * 100, num=related[i - 2]),
                    ha='center', va='bottom')
    # set metadata
    ax.set_ylabel('Number of videos')
    ax.set_title('Does a holiday event affect the YouTube trending tab?')
    ax.legend()
    # show plot
    plt.show()


def plot_5(dataframe):
    '''
    Author: Tuan
    '''
    # create empty string to hold all video titles later
    text = ''
    printable = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n'

    # filter all the titles to leave only printable characters
    dataframe['title'] = dataframe['title'].apply(
        lambda x: ''.join(filter(lambda xi: xi in printable, x)))
    # get each video title, break the words into tokens and add to 'text'
    for x in dataframe.index:
        title = str(dataframe.loc[x, 'title'])

        tokens = title.split()
        for i in range(len(tokens)):
            tokens[i] = tokens[i].lower()
        text += ' '.join(tokens)+' '

    # generate word cloud
    cloud = wordcloud.WordCloud(
        width=1400, height=800, background_color='white', min_font_size=10).generate(text)
    # plot the word cloud
    plt.figure(figsize=(8, 14), facecolor=None)
    plt.imshow(cloud)
    plt.axis("off")
    plt.tight_layout(pad=5)
    plt.show()
