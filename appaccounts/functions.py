from .models import Profile


def get_profile_description(user, fields=None):
    
    general_description = {
        'profile_id': '',
        'profile_name': '',
        'profile_description': '',
        'profile_avatar': '',
        'profile_url': '',
        'profile_created': '',
    }
        
    if user and user.profile:
        profile = user.profile
        general_description['profile_id'] = profile.id
        general_description['profile_name'] = user.username
        general_description['profile_description'] = profile.description if profile.description else 'Пользователь пока ничего не написал о себе'
        general_description['profile_avatar'] = profile.avatar.url if profile.avatar else ''
        general_description['profile_url'] = profile.get_absolute_url()
        general_description['profile_created'] = profile.created

    if fields:
        description = {}
        for field in fields:
            description[field] = general_description[field]
        return description
    else:
        return general_description