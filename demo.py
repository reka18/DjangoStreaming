import os

from conversation_manager.models import Comment
from demo_strings import header, intro, users_intro, documents_intro, modify_document_intro, follow_intro
from document_manager.models import Document
from document_manager.models import Status
from user_manager.models import StreamUser
from actstream.actions import follow, unfollow
from actstream.models import Follow


def create_user() -> None:
    username = input('Username: ')
    password = input('Password: ')
    again = input('Password (again): ')
    if password != again:
        print('Passwords do not match.')
        return
    email = input('Email: ')
    try:
        user = StreamUser.objects.create_user(username, email, password)
        user.save()
    except Exception as _:
        print('An exception occurred')


def list_users():
    print('-- User List --')
    users = StreamUser.objects.all()
    for user in users:
        print(f': {user.string()}')
    if len(users) == 0:
        print(': You have not created any users.')


def list_documents():
    print('-- Document List --')
    documents = Document.objects.all()
    for document in documents:
        print(f': {document.string()}')
    if len(documents) == 0:
        print(': You have not created any documents.')


def list_comments(document_id: str) -> bool:
    print('-- Comment List --')
    comments = Comment.objects.get(ref_document=document_id)
    print(f': {comments.string()}')


def list_follows(user: str) -> bool:
    print('-- Follow List --')
    follows = Follow.objects.all()
    follows = follows.filter(user=user)
    if len(follows) == 0:
        print(': You are not following anyone.')
    else:
        for follow in follows:
            print(f': {follow}')


def modify_document(updater: StreamUser, changes: {}, document_id: str) -> Document:
    document = Document.objects.get(id=document_id)
    if "title" in changes:
        updater.change_title(document, changes["title"])
    if "text" in changes:
        updater.change_text(document, changes["text"])
    if "status" in changes:
        updater.change_status(document, changes["status"])
    if "assignee" in changes:
        updater.change_assignee(document, changes["assignee"])


def clear():
    os.system('clear')


def press_enter():
    input(': Press Enter to continue...')


def main():
    active_user: StreamUser = StreamUser.objects.get(id=1)

    finished = False
    while not finished:
        clear()
        print(header)
        print(f': Note, you are logged in as \'{active_user.username}\'.')
        result = input(intro)
        if result in ['Q', 'q']:
            finished = True

        # USER HANDLER
        elif result == '1':
            user_finished = False
            while not user_finished:
                clear()
                user_result = input(users_intro)

                # BACK
                if user_result in ['B', 'b']:
                    user_finished = True

                # QUIT
                elif user_result in ['Q', 'q']:
                    user_finished = True
                    finished = True

                # CREATE USER
                if user_result == '1':
                    clear()
                    print('** Create User **')
                    create_user()
                    print(': You have a new user you can switch to.')
                    press_enter()

                # LIST USERS
                if user_result == '2':
                    clear()
                    print('** List Users **')
                    list_users()
                    press_enter()

                # SWITCH ACTIVE USER
                if user_result == '3':
                    clear()
                    print('** Switch Active User **')
                    list_users()
                    try:
                        user_id = input(': ID? ')
                        active_user = StreamUser.objects.get(id=user_id)
                        print(f': Active user is now \'{active_user.username}\'')
                    except Exception as _:
                        print(': Cancelled.')
                    press_enter()

                # FOLLOW
                if user_result == '4':
                    follow_finished = False
                    while not follow_finished:
                        clear()
                        follow_result = input(follow_intro)

                        # BACK
                        if follow_result in ['B', 'b']:
                            follow_finished = True

                        # QUIT
                        elif follow_result in ['Q', 'q']:
                            follow_finished = True
                            user_finished = True
                            finished = True

                        # FOLLOW
                        if follow_result == '1':
                            clear()
                            switch = input(': Follow User or Document? (U/D) ')
                            if switch in ['U', 'u']:
                                print('** Follow User **')
                                list_users()
                                try:
                                    user_id = input(': ID? ')
                                    actor_only = input(': Actor Only? (Y/N) ')
                                    if actor_only in ['Y', 'y']:
                                        actor_only = True
                                    else:
                                        actor_only = False
                                    user_to_follow = StreamUser.objects.get(id=user_id)
                                    follow(active_user, user_to_follow, send_action=True, actor_only=actor_only)
                                    print(f': You are now following \'{user_to_follow.username}\'.')
                                except Exception as _:
                                    print(': Cancelled.')
                                press_enter()
                            elif switch in ['D', 'd']:
                                print('** Follow Document **')
                                list_documents()
                                try:
                                    document_id = input(': ID? ')
                                    actor_only = input(': Actor Only? (Y/N) ')
                                    if actor_only in ['Y', 'y']:
                                        actor_only = True
                                    else:
                                        actor_only = False
                                    document_to_follow = Document.objects.get(id=document_id)
                                    follow(active_user, document_to_follow, send_action=True, actor_only=actor_only)
                                    print(f': You are now following \'{document_to_follow.title}\'.')
                                except Exception as _:
                                    print(': Cancelled.')
                                press_enter()
                            else:
                                print(': Cancelled.')
                                press_enter()

                        # LIST FOLLOWS
                        if follow_result == '2':
                            clear()
                            print('** List Follows **')
                            list_follows(user=active_user)
                            press_enter()

                        # UNFOLLOW USER
                        if follow_result == '3':
                            clear()
                            print('** Unfollow User **')
                            list_follows(user=active_user)
                            switch = input(': Unfollow User or Document? (U/D) ')
                            if switch in ['U', 'u']:
                                print('** Unfollow User **')
                                list_users()
                                try:
                                    user_id = input(': ID? ')
                                    user_to_unfollow = StreamUser.objects.get(id=user_id)
                                    unfollow(active_user, user_to_unfollow)
                                    print(f': You are no longer following \'{user_to_unfollow.username}\'.')
                                except Exception as _:
                                    print(': Cancelled.')
                                press_enter()
                            elif switch in ['D', 'd']:
                                print('** Unfollow Document **')
                                list_documents()
                                try:
                                    document_id = input(': ID? ')
                                    document_to_unfollow = Document.objects.get(id=document_id)
                                    unfollow(active_user, document_to_unfollow)
                                    print(f': You are no longer following \'{document_to_unfollow.title}\'.')
                                except Exception as _:
                                    print(': Cancelled.')
                                press_enter()
                # MESSAGE OTHER USER
                if user_result == '5':
                    clear()
                    print('** Message User **')
                    list_users()
                    try:
                        user_id = input(': ID? ')
                        recipient = StreamUser.objects.get(id=user_id)
                        message = input(': Message? ')
                        active_user.message(recipient=recipient, message=message)
                        print(f': Message sent to \'{recipient.username}\'.')
                    except Exception as e:
                        print(e)
                        print(': Cancelled.')
                    press_enter()

        # DOCUMENT HANDLER
        elif result == '2':
            document_finished = False
            while not document_finished:
                clear()
                document_result = input(documents_intro)

                # BACK
                if document_result in ['B', 'b']:
                    document_finished = True

                # QUIT
                elif document_result in ['Q', 'q']:
                    document_finished = True
                    finished = True

                # CREATE DOCUMENT
                if document_result == '1':
                    clear()
                    print('** Create Document **')
                    title = input('Title: ')
                    text = input('Text: ')
                    active_user.create_document(title, text, [])
                    print(': You have a new document.')
                    press_enter()

                # LIST DOCUMENTS
                if document_result == '2':
                    clear()
                    print('** List Documents **')
                    list_documents()
                    press_enter()

                # TAG DOCUMENT
                if document_result == '3':
                    clear()
                    print('** Add Tag **')
                    list_documents()
                    document_id = input(': ID? ')
                    tag = input(': Tag? ')
                    if input(': Press ENTER to confirm or any other key to cancel.') == '':
                        document: Document = Document.objects.get(id=document_id)
                        active_user.add_tag(document=document, text=tag)
                        print(': Tag added.')
                    else:
                        print(': Cancelled.')
                    press_enter()

                # VOTE ON DOCUMENT
                if document_result == '4':
                    clear()
                    print('** Vote on Document **')
                    list_documents()
                    document_id = input(': ID? ')
                    vote = input(': Vote? ')
                    if vote in ['up', 'down']:
                        document: Document = Document.objects.get(id=document_id)
                        if vote == 'up':
                            active_user.up_vote(target=document)
                            print(': Vote added.')
                        elif vote == 'down':
                            active_user.down_vote(target=document)
                            print(': Vote added.')
                        else:
                            print(': Cancelled.')
                    else:
                        print(': Cancelled.')
                    press_enter()

                # MODIFY DOCUMENT
                if document_result == '5':
                    modify_finished = False
                    while not modify_finished:
                        clear()
                        modify_result = input(modify_document_intro)

                        # BACK
                        if modify_result in ['B', 'b']:
                            modify_finished = True

                        # QUIT
                        elif modify_result in ['Q', 'q']:
                            modify_finished = True
                            finished = True

                        if modify_result == '1':
                            clear()
                            print('** Change Title **')
                            list_documents()
                            document_id = input(': ID? ')
                            title = input(': Title? ')
                            modify_document(active_user, {"title": title}, document_id)
                            print(': Document modified.')
                            press_enter()

                        if modify_result == '2':
                            clear()
                            print('** Change Text **')
                            list_documents()
                            document_id = input(': ID? ')
                            text = input(': Text? ')
                            modify_document(active_user, {"text": text}, document_id)
                            print(': Document modified.')
                            press_enter()

                        if modify_result == '3':
                            clear()
                            print('** Change Status **')
                            list_documents()
                            document_id = input(': ID? ')
                            status = input(
                                'BACKLOG = 1\n' +
                                'OPEN = 2\n' +
                                'TODO = 3\n' +
                                'IN_PROGRESS = 4\n' +
                                'IN_REVIEW = 5\n' +
                                'DONE = 6\n' +
                                'CLOSED = 7\n'
                            )
                            if status == '1':
                                status = Status.BACKLOG
                            elif status == '2':
                                status = Status.OPEN
                            elif status == '3':
                                status = Status.TODO
                            elif status == '4':
                                status = Status.IN_PROGRESS
                            elif status == '5':
                                status = Status.IN_REVIEW
                            elif status == '6':
                                status = Status.DONE
                            elif status == '7':
                                status = Status.CLOSED
                            else:
                                status = None
                            if status:
                                modify_document(active_user, {"status": status}, document_id)
                                print(': Document modified.')
                            else:
                                print(': Cancelled.')
                            press_enter()

                        if modify_result == '4':
                            clear()
                            print('** Change Assignee **')
                            list_documents()
                            document_id = input(': ID? ')
                            clear()
                            list_users()
                            assignee = input(': ID? ')
                            if assignee != '':
                                assignee = StreamUser.objects.get(id=assignee)
                                modify_document(active_user, {"assignee": assignee}, document_id)
                                print(': Document modified.')
                            else:
                                print(': Cancelled.')
                            press_enter()

                # COMMENT ON DOCUMENT
                if document_result == '6':
                    clear()
                    print('** Add Comment **')
                    list_documents()
                    document_id = input('ID: ')
                    text = input('Text: ')
                    clear()
                    document = Document.objects.get(id=document_id)
                    active_user.comment(document, text)
                    print(': Comment added.')
                    press_enter()

                # LIST COMMENTS ON DOCUMENT
                if document_result == '7':
                    clear()
                    print('** List Comments **')
                    list_documents()
                    document_id = input(': ID? ')
                    clear()
                    list_comments(document_id=document_id)
                    press_enter()

                # REPLY TO COMMENT
                if document_result == '8':
                    clear()
                    print('** Reply to Comment **')
                    list_documents()
                    document_id = input(': Document ID? ')
                    clear()
                    list_comments(document_id=document_id)
                    comment_id = input(': Comment ID? ')
                    text = input(': Text? ')
                    comment = Comment.objects.get(id=comment_id)
                    active_user.reply(comment, text)
                    print(': Reply added.')
                    press_enter()

                # VOTE ON COMMENT
                if document_result == '9':
                    clear()
                    print('** Vote on Comment **')
                    list_documents()
                    document_id = input(': Document ID? ')
                    clear()
                    list_comments(document_id=document_id)
                    comment_id = input(': Comment ID? ')
                    vote = input(': Vote? ')
                    if vote in ['up', 'down']:
                        comment: Comment = Comment.objects.get(id=comment_id)
                        if vote == 'up':
                            active_user.up_vote(target=comment)
                            print(': Vote added.')
                        elif vote == 'down':
                            active_user.down_vote(target=comment)
                            print(': Vote added.')
                        else:
                            print(': Cancelled.')
                    else:
                        print(': Cancelled.')
                    press_enter()

        else:
            continue


main()
