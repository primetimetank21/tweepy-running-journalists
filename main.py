from secrets import API_KEY, API_SECRET_KEY, BEARER_TOKEN, ACCESS_TOKEN_SECRET, ACCESS_TOKEN
import tweepy
import csv

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# q = "runner journalist -up lang:en"
queries = ["runner journalist", "runner blogger", "runner reporter"]
interesting_users = []
prev_users_list   = {}
for key in queries:
    prev_users_list[key] = []
done = False
people_limit = 1000
print("Getting users...")

for i in range(1, 51):
    for q in queries:
        try:
            print(f"    {q}: page {i}", end=" ")
            res = api.search_users(q, 20, i)
            if i == 1:
                interesting_users  += res
                prev_users_list[q]  = res
                continue

            try:
                print(f"({prev_users_list[q][0].id} __ {res[0].id})")
            except:
                print("Couldn't compare")


            if prev_users_list[q][0].id != res[0].id:
                interesting_users  += res
                prev_users_list[q]  = res
                
            if len(interesting_users) >= people_limit:
                done = True
                break
        except Exception as e:
            print(f"    Error: {e}")
    if done == True:
        break



# with open("users.txt", "w") as f:
#     for user in interesting_users:
#         f.write(str(user) + '\n')
        
with open("handles.txt", "w") as f:
    user_names = [user.screen_name for user in interesting_users]    
    for name in sorted(user_names):
        f.write(name + '\n')
print(len(list(set(user_names))))


master_list = []
for user in interesting_users:
    user_data = {
        "Name":              user.name,
        "Twitter Handle":    user.screen_name,
        "Location":          user.location,
        "Followers":         user.followers_count,
        "Following":         user.friends_count,
        "Description":       user.description.strip().replace('\n', ' '),
        "Profile Image URL": user.profile_image_url_https,
    }
    master_list.append(user_data)

# with open("journalists_2.tsv", "w") as f:
#     fields = ["Name", "Twitter Handle", "Location", "Followers", "Following", "Description", "Profile Image URL"]
#     writer = csv.DictWriter(f, delimiter='\t', fieldnames=fields)
#     writer.writeheader()
#     writer.writerows(master_list)


print("Done")