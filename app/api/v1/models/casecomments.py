#######################################################################################################################
#                                                                                                                     #
# Copyright (c) 2018 Qualcomm Technologies, Inc.                                                                      #
#                                                                                                                     #
# All rights reserved.                                                                                                #
#                                                                                                                     #
# Redistribution and use in source and binary forms, with or without modification, are permitted (subject to the      #
# limitations in the disclaimer below) provided that the following conditions are met:                                #
# * Redistributions of source code must retain the above copyright notice, this list of conditions and the following  #
#   disclaimer.                                                                                                       #
# * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the         #
#   following disclaimer in the documentation and/or other materials provided with the distribution.                  #
# * Neither the name of Qualcomm Technologies, Inc. nor the names of its contributors may be used to endorse or       #
#   promote products derived from this software without specific prior written permission.                            #
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY THIS LICENSE. THIS SOFTWARE IS PROVIDED  #
# BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED #
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT      #
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR   #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES LOSS OF USE,      #
# DATA, OR PROFITS OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,      #
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,   #
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                                                                  #
#                                                                                                                     #
#######################################################################################################################

from app import db


class CaseComments(db.Model):
    """Database model for case comments"""
    id = db.Column(db.Integer, primary_key=True)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id', ondelete='CASCADE'))
    comments = db.Column(db.Text)
    comment_date = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.String(100))
    username = db.Column(db.String(1000))

    def __init__(self, comment_text, case_id, user_id, username):
        """Constructor"""
        self.comments = comment_text
        self.case_id = case_id
        self.user_id = user_id
        self.username = username

    def __repr__(self):
        return '%r' % self.id

    @property
    def serialize(self):
        """Serialize data."""
        return {
            "user_id": self.user_id,
            "comment": self.comments,
            "username": self.username,
            "comment_date": self.comment_date
        }

    @staticmethod
    def __get_id(instr_obj):
        """return string value from instrumented list object."""
        try:
            if len(instr_obj) > 0:
                return str(instr_obj[0])
            return None
        except Exception:
            raise Exception

    @staticmethod
    def get(record_id):
        """retrieve data by id"""
        try:
            if record_id:
                comment = CaseComments.query.filter_by(id=record_id).first()
                return comment.serialize
            return []
        except Exception:
            raise Exception

    @classmethod
    def add(cls, case_comment, case_id, user_id, username):
        """Insert data"""
        try:
            comment = cls(case_comment, case_id, user_id, username)
            db.session.add(comment)
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise Exception

