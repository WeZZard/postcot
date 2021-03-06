from typing import Dict

from django import forms
from django.contrib.admin import widgets as admin_widgets

from postcot_core.models import AccessAction


class AccessActionForm(forms.ModelForm):
    action: str = forms.CharField(
        label='Action',
        max_length=256,
        widget=admin_widgets.AdminTextInputWidget,
        help_text='''
<h5>Accept Actions</h5>
<dl compact>
    <dt><span class="postfix_keyword"><span class="fixed">OK</span></span></dt>
    <dd>
        <p>
            Accept the address etc. that matches the pattern.
        </p>
    </dd>
    <dt><span class="postfix_keyword">all-numerical</span></dt>
    <dd>
        <p>
            An all-numerical result is treated as 
            <span class="postfix_keyword"><span class="fixed">OK</span>
            </span>. This format is generated by address-based relay 
            authorization schemes such as pop-before-smtp.
        </p>
    </dd>
</dl>
<h5>Reject Actions</h5>
<dl compact>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">4</span><span class="dynamic">NN</span>
        </span>
        <span class="postfix_user_string"> text</span>
    </dt>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">5</span><span class="dynamic">NN</span>
        </span>
        <span class="postfix_user_string"> text</span>
    </dt>
    <dd>
        <p>
            Reject the address etc. that matches the pattern, and respond 
            with the numerical three-digit code and text. 
            <span class="postfix_keyword">
                <span class="fixed">4</span><span class="dynamic">NN</span>
            </span> means "try again 
            later", while 
            <span class="postfix_keyword">
                <span class="fixed">5</span><span class="dynamic">NN</span>
            </span> means "do not try again".
        </p>
        <p>
            The following responses have special meaning for the Postfix 
            SMTP server:
        </p>
        <dl>
            <dt>
                <span class="postfix_keyword">
                    <span class="fixed">421</span>
                </span> text (Postfix 2.3 and later)
            </dt>
            <dt>
                <span class="postfix_keyword">
                    <span class="fixed">521</span>
                </span> text (Postfix 2.6 and later)</dt>
            <dd>
                <p>
                    After responding with the numerical three-digit code 
                    and text, disconnect immediately from the SMTP client.
                    This frees up SMTP server resources so that they can 
                    be made available to another SMTP client.
                </p>
                <p>
                    Note: The "521" response should be used only with 
                    botnets and other malware where interoperability is 
                    of no concern. The  "send  521  and  disconnect" 
                    behavior is NOT defined in the SMTP standard.
                </p>
            </dd>
        </dl>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">REJECT</span>
        </span>
        <span class="postfix_user_string">
            optional text...
        </span>
    </dt>
    <dd>
        <p>
            Reject the address etc. that matches the pattern. Reply with
            "<span class="postfix_keyword"><span class="fixed">$access_map_reject_code</span></span><span class="postfix_user_string"> optional text...</span>"
            when the optional text is specified, otherwise reply with a 
            generic error response message.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">DEFER</span>
        </span>
        <span class="postfix_user_string">
            optional text...
        </span>
    </dt>
    <dd>
        <p>
            Reject the address etc. that matches the pattern. Reply with 
            "<span class="postfix_keyword"><span class="fixed">$access_map_defer_code</span></span><span class="postfix_user_string"> optional text...</span>"
            when the optional text is specified, otherwise reply with a 
            generic error response message.
        </p> 
        <p>
            This feature is available in Postfix 2.6 and later.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">DEFER_IF_REJECT</span>
        </span>
        <span class="postfix_user_string">
            optional text...
        </span>
    </dt>
    <dd>
        <p>
            Defer the request if some later restriction would result in a
            <span class="postfix_keyword"><span class="fixed">REJECT</span></span>
            action. Reply with 
            "<span class="postfix_keyword"><span class="fixed">$access_map_defer_code 4.7.1</span></span><span class="postfix_user_string"> optional text...</span>"
            when the optional text is specified, otherwise reply with a 
            generic error response message.
        </p> 
        <p>
            Prior to Postfix 2.6, the SMTP reply code is 450.
        </p>
        <p>
            This feature is available in Postfix 2.1 and later.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">DEFER_IF_PERMIT</span>
        </span>
        <span class="postfix_user_string">
            optional text...
        </span>
    </dt>
    <dd>
        <p>
            Defer the request if some later restriction would result in an 
            explicit or implicit 
            <span class="postfix_keyword"><span class="fixed">PERMIT</span></span> 
            action. Reply with
            "<span class="postfix_keyword"><span class="fixed">$access_map_defer_code 4.7.1</span></span><span class="postfix_user_string"> optional text...</span>" 
            when the optional text is specified, otherwise reply with a
            generic error response message.
        </p> 
        <p>
            Prior to Postfix 2.6, the SMTP reply code is 450.
        </p>
        <p>
            This feature is available in Postfix 2.1 and later.
        </p>
    </dd>
</dl>
<h5>Other Actions</h5>
<dl compact>
    <dt>
        <span class="postfix_keyword">
            <span class="dynamic">restriction...</span>
        </span>
    </dt>
    <dd>
        <p>
            Apply the named UCE 
            <span class="postfix_keyword"><span class="fixed">restriction</span></span>(s)
            (<span class="postfix_keyword"><span class="fixed">permit</span></span>, 
            <span class="postfix_keyword"><span class="fixed">reject</span></span>,
            <span class="postfix_keyword"><span class="fixed">reject_unauth_destination</span></span>, and so on).
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">BCC</span>
        </span>
        <span class="postfix_user_string">
            user@domain
        </span>
    </dt>
    <dd>
        <p>
            Send one copy of the message to the specified recipient.
        </p>
        <p>
            If multiple 
            <span class="postfix_keyword"><span class="fixed">BCC</span></span> 
            actions are specified within the same SMTP 
            MAIL transaction, only the last action will be used.
        </p>
        <p>
            This feature is not part of the stable Postfix release.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">DISCARD</span>
        </span>
        <span class="postfix_user_string">
            optional text...
        </span>
    </dt>
    <dd>
        <p>
            Claim successful delivery and silently discard the message. 
            Log the optional text if specified, otherwise log a generic 
            message.
        </p>
        <p>
            Note: this action currently affects all recipients of the 
            message. To discard only one recipient without discarding the 
            entire message, use the transport(5) table to direct mail to 
            the discard(8) service.
        </p>
        <p>
            This feature is available in Postfix 2.0 and later.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">DUNNO</span>
        </span>
    <dd>
        <p>
            Pretend that the lookup key was not found. This prevents 
            Postfix from trying substrings of the lookup key (such as a
            subdomain name, or a network address subnetwork).
        </p>
        <p>
            This feature is available in Postfix 2.0 and later.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">FILTER</span>
        </span>
        <span class="postfix_user_string">
            transport:destination
        </span>
    </dt>
    <dd>
        <p>
            After the message is queued, send the entire message through 
            the specified external content filter. The 
            transport:destination syntax is described in the transport(5)
            manual page. More information about external content filters 
            is in the Postfix FILTER_README file.
        </p>
        <p>
            Note: this action overrides the content_filter setting, and
            currently affects all recipients of the message.
        </p>
        <p>
            This feature is available in Postfix 2.0 and later.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">HOLD</span>
        </span>
        <span class="postfix_user_string">
            optional text...
        </span>
    </dt>
    <dd>
        <p>
            Place the message on the hold queue, where it will sit until 
            someone either deletes it or releases it for delivery. Log the 
            optional text if specified, otherwise log a generic message.
        </p>
        <p>
            Mail that is placed on hold can be examined with the 
            postcat(1) command, and can be destroyed or released with the 
            postsuper(1) command.
        </p>
        <p>
            Note: use "postsuper -r" to release mail that was kept on hold 
            for a significant fraction of 
            <span class="postfix_keyword"><span class="fixed">$maximal_queue_lifetime</span></span> or 
            <span class="postfix_keyword"><span class="fixed">$bounce_queue_lifetime</span></span>, 
            or longer. Use "postsuper -H" only for mail that will not 
            expire within a few delivery attempts.
        </p>
        <p>
           Note: this action currently affects all recipients of the 
           message.
        </p>
        <p>
           This feature is available in Postfix 2.0 and later.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">PREPEND</span>
        </span>
        <span class="postfix_user_string">
            headername: headervalue
        </span>
    </dt>
    <dd>
        <p>
            Prepend the specified message header to the message. When more 
            than one 
            <span class="postfix_keyword"><span class="fixed">PREPEND</span></span>
            action executes, the first prepended header appears before the 
            second etc. prepended header.
        </p>
        <p>
            Note: this action must execute before the message content is 
            received; it cannot execute in the context of 
            smtpd_end_of_data_restrictions.
        </p>
        <p>
            This feature is available in Postfix 2.1 and later.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">REDIRECT</span>
        </span>
        <span class="postfix_user_string">
            user@domain
        </span>
    </dt>
    <dd>
        <p>
            After the message is queued, send the message to the specified 
            address instead of the intended recipient(s).
        </p>
        <p>
            Note: this action overrides the 
            <span class="postfix_keyword"><span class="fixed">FILTER</span></span> 
            action, and currently 
            affects all recipients of the message.
        </p>
        <p>
            This feature is available in Postfix 2.1 and later.
        </p>
    </dd>
    <dt>
        <span class="postfix_keyword">
            <span class="fixed">WARN</span>
        </span>
        <span class="postfix_user_string">
            optional text...
        </span>
    </dt>
    <dd>
        <p>
            Log a warning with the optional text, together with client 
            information and if available, with helo, sender, recipient and 
            protocol information.
        </p>
        <p>
            This feature is available in Postfix 2.1 and later.
        </p>
    </dd>
</dl>
'''
    )

    def clean(self) -> Dict[str, str]:
        cleaned_data = super().clean()
        return cleaned_data

    class Meta:
        model = AccessAction
        fields = ['action', 'notes']

    class Media:
        css = {
            'all': ('postcot/admin/css/change_form_help_text_postfix.css',),
        }
