import csv
import random

topics = [
    ('Machine Learning', 'machine learning, AI, algorithms, data science, neural networks'),
    ('Data Science', 'data science, python, pandas, analysis, visualization'),
    ('Web Development', 'web development, javascript, react, node.js, frontend'),
    ('Python Programming', 'python, programming, coding, software development'),
    ('Deep Learning', 'deep learning, neural networks, tensorflow, pytorch, AI'),
    ('Cloud Computing', 'cloud computing, AWS, Azure, infrastructure, DevOps'),
    ('Cybersecurity', 'cybersecurity, security, hacking, encryption, privacy'),
    ('Mobile Development', 'mobile development, iOS, Android, React Native, Flutter'),
    ('Blockchain', 'blockchain, cryptocurrency, bitcoin, ethereum, smart contracts'),
    ('DevOps', 'DevOps, CI/CD, Docker, Kubernetes, automation'),
    ('Natural Language Processing', 'NLP, text analysis, language models, transformers'),
    ('Computer Vision', 'computer vision, image processing, OpenCV, deep learning'),
    ('Database Design', 'database, SQL, NoSQL, MongoDB, PostgreSQL'),
    ('Software Architecture', 'software architecture, design patterns, system design'),
    ('API Development', 'API, REST, GraphQL, microservices, backend'),
    ('Frontend Frameworks', 'React, Vue, Angular, frontend, JavaScript'),
    ('Backend Development', 'backend, server, API, Node.js, Python'),
    ('Data Engineering', 'data engineering, ETL, pipelines, big data'),
    ('Machine Learning Operations', 'MLOps, model deployment, production ML'),
    ('Quantum Computing', 'quantum computing, quantum algorithms, Qiskit'),
    ('Technology', 'technology, innovation, tech, digital transformation, IT'),
    ('Artificial Intelligence', 'AI, artificial intelligence, machine learning, automation'),
    ('Software Engineering', 'software engineering, coding, development, programming'),
]

authors = [
    ('John Doe', 'https://medium.com/@johndoe'),
    ('Jane Smith', 'https://medium.com/@janesmith'),
    ('Bob Johnson', 'https://medium.com/@bobjohnson'),
    ('Alice Williams', 'https://medium.com/@alicewilliams'),
    ('Charlie Brown', 'https://medium.com/@charliebrown'),
    ('Diana Prince', 'https://medium.com/@dianaprince'),
    ('Edward Norton', 'https://medium.com/@edwardnorton'),
    ('Fiona Apple', 'https://medium.com/@fionaapple'),
    ('George Lucas', 'https://medium.com/@georgelucas'),
    ('Hannah Montana', 'https://medium.com/@hannahmontana'),
]

def generate_article(index):
    topic, keywords = random.choice(topics)
    author_name, author_url = random.choice(authors)
    
    title_variations = [
        f'Introduction to {topic}',
        f'{topic}: A Complete Guide',
        f'Mastering {topic}',
        f'{topic} Fundamentals',
        f'Advanced {topic} Techniques',
        f'Getting Started with {topic}',
        f'{topic} Best Practices',
        f'Understanding {topic}',
        f'{topic} Tutorial',
        f'{topic} Explained',
    ]
    
    subtitle_variations = [
        f'Learn everything you need to know about {topic}',
        f'A comprehensive guide to {topic}',
        f'Everything you need to know about {topic}',
        f'Master {topic} from scratch',
        f'Deep dive into {topic}',
    ]
    
    title = random.choice(title_variations)
    subtitle = random.choice(subtitle_variations)
    
    text_samples = [
        f'{topic} is a fascinating field that combines theory and practice. In this article, we explore the fundamentals and advanced concepts.',
        f'This comprehensive guide to {topic} covers everything from basics to advanced techniques. Learn how to apply these concepts in real-world scenarios.',
        f'Whether you are a beginner or an expert, this article on {topic} will provide valuable insights and practical examples.',
        f'{topic} has revolutionized the way we approach problems. Discover the key concepts and best practices in this detailed guide.',
        f'In this article, we dive deep into {topic}, exploring its applications, benefits, and implementation strategies.',
    ]
    
    text = random.choice(text_samples)
    
    num_images = random.randint(2, 8)
    num_external_links = random.randint(3, 15)
    claps = random.randint(100, 15000)
    reading_time = random.randint(5, 20)
    
    image_urls = '; '.join([f'https://example.com/img{i+1}.jpg' for i in range(num_images)])
    
    url_slug = title.lower().replace(' ', '-').replace(':', '').replace(',', '')
    url = f'https://medium.com/@{author_name.split()[0].lower()}/{url_slug}-{index}'
    
    return {
        'url': url,
        'title': title,
        'subtitle': subtitle,
        'text': text,
        'num_images': num_images,
        'image_urls': image_urls,
        'num_external_links': num_external_links,
        'author_name': author_name,
        'author_url': author_url,
        'claps': claps,
        'reading_time': reading_time,
        'keywords': keywords
    }

def create_1000_articles_csv(filename='scrapping_results.csv'):
    fieldnames = [
        'url', 'title', 'subtitle', 'text', 'num_images', 'image_urls',
        'num_external_links', 'author_name', 'author_url', 'claps',
        'reading_time', 'keywords'
    ]
    
    print(f"Generating 1000 sample articles...")
    print("This may take a moment...")
    
    articles = []
    for i in range(1, 1001):
        articles.append(generate_article(i))
        if i % 100 == 0:
            print(f"Generated {i}/1000 articles...")
    
    print(f"Writing to {filename}...")
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(articles)
    
    print(f"[OK] Successfully created {filename} with 1000 articles!")
    print(f"\nStatistics:")
    print(f"  Total articles: 1000")
    print(f"  Total claps: {sum(a['claps'] for a in articles):,}")
    print(f"  Average claps: {sum(a['claps'] for a in articles) // 1000}")
    print(f"  Average reading time: {sum(a['reading_time'] for a in articles) / 1000:.1f} minutes")
    print(f"\nNext steps:")
    print(f"1. Restart your API: python api.py")
    print(f"2. Test search with: python test_api.py")

if __name__ == '__main__':
    create_1000_articles_csv()
